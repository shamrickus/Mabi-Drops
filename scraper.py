import json, xmltodict, MySQLdb
from config import *

items = []
monsters = []
monster_drops = []
drop_table = dict()
affixs = []
manuals = []

def populate(pTable):
	for dType in ["Drop1", "Drop2", "Drop3"]:
		drops = pTable[dType].replace("(", "").replace(")", "").split(';')
		for drop in drops:
			itemAttrs = drop.split(" ")

			iId = ""
			for attr in itemAttrs:
				fullAttr = attr.split(":")

				if fullAttr[0] == "id":
					iId = fullAttr[1]

					drop_table[iId] = dict()
					drop_table[iId]["monster_id"] = (pTable["TypeID"])
					drop_table[iId]["item_id"] = (iId)
					drop_table[iId]["probability"] = repr( (int(drop_table[iId]["probability"]) + 1) if "probability" in drop_table[iId] else 1)
					drop_table[iId]["drop_tier"] = repr(1)

				elif fullAttr[0] == "manual":
					iId = fullAttr[1]

					drop_table[iId] = dict()
					drop_table[iId]["monster_id"] = (pTable["TypeID"])
					drop_table[iId]["manual_id"] = (fullAttr[1])
					drop_table[iId]["probability"] = repr( (int(drop_table[iId]["probability"]) + 1) if "probability" in drop_table[iId] else 1)
					drop_table[iId]["drop_tier"] = repr(1)

				elif fullAttr[0] == "suffix":
					drop_table[iId]["suffix_id"] = (fullAttr[1])

				elif fullAttr[0] == "prefix":
					drop_table[iId]["prefix_id"] = (fullAttr[1])
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
			'drop_one':		value["Drop1Rate"],
			'drop_two':		value["Drop2Rate"],
			'drop_three':	value["Drop3Rate"]
		}
	)

	populate(value)


with open('Drop-Table/itemdb.xml') as file:
	data = xmltodict.parse(file.read())

for item in data["Items"]["Mabi_Item"]:
	items.append({
		"item_id": (item["@ID"]),
		"name": repr(item["@Text_Name0"]) if "@Text_Name0" in item else ""
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

db = MySQLdb.connect(host=config["host"], user=config["user"], password=config["password"], db=config["db"])

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


for drop in drop_table:
	num = 3
	drops = drop_table[drop]
	tup = ( drops["monster_id"], drops["drop_tier"], drops["probability"] )
	query = "INSERT INTO `drop_table`(monster_id, drop_tier, probability, "
	#monster_id, drops_tier, probability, item_id, manual_id, prefix_id, suffix_id) \"
	if "item_id" in drops:
		query += "item_id"
		tup = tup + (drops["item_id"],)
	if "manual_id" in drops:
		query += "manual_id"
		tup = tup + (drops["manual_id"],)
	if "prefix_id" in drops:
		query += ", prefix_id"
		tup = tup + (drops["prefix_id"],)
		num += 1
	if "suffix_id" in drops:
		query += ", suffix_id"
		tup = tup + (drops["suffix_id"],)
		num += 1
	query += ") VALUES(%s"
	for i in range(num):
		query += ", %s"
	query += ")"

	cur.execute(query, tup)

db.commit()
db.close()
