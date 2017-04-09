import MySQLdb
from config import *
from db import *

def getDb():
	global config
	db = DB(host=config["host"], user=config["user"], password=config["password"], database=config["db"])
	db.connectDB()
	return db

conn = getDb()
query = """
	SELECT 	item.name, 
			drop_table.probability, 
			drop_table.drop_tier 
	FROM drop_table 
	join item 
		on item.item_id = drop_table.item_id 
	WHERE monster_id = %s 
	and drop_table.item_id is not null
"""

result = conn.select(query, [str(987)])
print(result)