import json, xmltodict, MySQLdb
from config import config
from db import reset

items = []
monsters = []
monster_drops = []
drop_table = dict()
affixs = []
manuals = []

reset(config)

#drop_table -> monster -> tier -> item -> { prob, prefix, suffix, type }
def populate(pTable):
	for dType in ["Drop1", "Drop2", "Drop3"]:
		if  len(pTable[dType]) < 1:
			continue

		if pTable["TypeID"] not in drop_table:
			drop_table[pTable["TypeID"]] = dict()
		if int(dType[-1:]) not in drop_table[pTable["TypeID"]]:
			drop_table[pTable["TypeID"]][int(dType[-1:])] = dict()

		drops = pTable[dType].replace("(", "").replace(")", "").split(';')
		for drop in drops:
			itemAttrs = drop.split(" ")
			iId = None
			for attr in itemAttrs:
				fullAttr = attr.split(":")

				if fullAttr[0] in ["id", "manual"]:
					iId = fullAttr[1]

					if iId in drop_table[pTable["TypeID"]][int(dType[-1:])]:
						prob = int( drop_table[pTable["TypeID"]][int(dType[-1:])][iId]["prob"]) + 1
					else:
						prob = 1
						drop_table[pTable["TypeID"]][int(dType[-1:])][iId] = dict()

					if fullAttr[0] == "id":
						iType = "item_id"
					else:
						iType = "manual_id"

					drop_table[pTable["TypeID"]][int(dType[-1:])][iId] = {
						'type': iType,
						'prob': prob
					}

				elif fullAttr[0] == "suffix":
					drop_table[pTable["TypeID"]][int(dType[-1:])][iId]["suffix_id"] = fullAttr[1]

				elif fullAttr[0] == "prefix":
					drop_table[pTable["TypeID"]][int(dType[-1:])][iId]["prefix_id"] = fullAttr[1]

with open('Drop-Table/itemdroptype.json') as file:
	data = json.load(file)

data = data["ItemDropTypeList"]

for key, value in data.items():
	monsters.append( 
		{
			'monster_id': 	(value["TypeID"]),
			'desc':			repr(value["Desc"]),
			'name':			repr(key)
		}
	)

	monster_drops.append(
		{
			'monster_id':	value["TypeID"],
			'drop_one':		value["Drop1Rate"] if "Drop1Rate" in value else 0,
			'drop_two':		value["Drop2Rate"] if "Drop2Rate" in value else 0,
			'drop_three':	value["Drop3Rate"] if "Drop3Rate" in value else 0
		}
	)

	populate(value)


with open('Drop-Table/itemdb.xml') as file:
	data = xmltodict.parse(file.read())

for item in data["Items"]["Mabi_Item"]:
	items.append({
		"item_id": (item["@ID"]),
		"name": repr(item["@Text_Name0"]) if "@Text_Name0" in item else "Unknown Name: " + str(item["@ID"])
	})

with open('Drop-Table/manualform.xml') as file:
	data = xmltodict.parse(file.read())

for group in data["ManualForm"]:
	for manual in data["ManualForm"][group]["ManualForm"]:
		manuals.append({
			"manual_id": manual["@FormID"],
			"name": manual["@ManualNameEng"]
		})

with open('Drop-Table/optionset.xml') as file:
	data = xmltodict.parse(file.read())


for affix in data["OptionSet"]["OptionSetList"]["OptionSet"]:
	affixs.append({
			"affix_id": affix["@ID"],
			"name": affix["@Name"]
		})

db = MySQLdb.connect(host=config["host"], user=config["user"], passwd=config["password"], db=config["db"])

cur = db.cursor()

query = "INSERT INTO affix(name, affix_id) VALUES(%s, %s)"
for affix in affixs:
	cur.execute(query, (affix["name"], affix["affix_id"]))

query = "INSERT INTO manual(name, manual_id) VALUES(%s, %s)"
for manual in manuals:
	cur.execute(query, (manual["name"], manual["manual_id"]))

query = "INSERT INTO item(item_id, name) VALUES(%s, %s)"
for item in items:
	cur.execute(query, (item["item_id"], item["name"]))

query = "INSERT INTO monster(monster_id, `desc`, name) VALUES(%s, %s, %s)"
for monster in monsters:
	cur.execute(query, (monster["monster_id"], monster["desc"], monster["name"]))

query = "INSERT INTO monster_drop(monster_id, drop_one, drop_two, drop_three) VALUES(%s, %s, %s, %s)"

for drop in monster_drops:
	cur.execute(query, (drop["monster_id"], drop["drop_one"], drop["drop_two"], drop["drop_three"]))


#drop_table -> monster -> tier -> item -> { prob, prefix, suffix, type }
entries = 0
for monster in drop_table:
	for drop in drop_table[monster]:
		for iId in drop_table[monster][drop]:
			num = 3
			query = "INSERT INTO `drop_table`(monster_id, drop_tier, probability, "

			value = drop_table[monster][drop][iId]

			if value["type"] not in query:
				query += value["type"]

			tup = ( monster, drop, value["prob"], int(iId) )

			for modify in ["suffix_id", "prefix_id"]:
				if modify in value:
					tup = tup + (value[modify],)
					if modify not in query:
						num += 1
						query += ", " + modify

			query += ") VALUES(%s"
			for i in range(num):
				query += ", %s"
			query += ")"
			cur.execute(query, tup)
			entries+= 1

print "Inserted " + str(entries)

db.commit()
db.close()
