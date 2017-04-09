from flask import Flask, render_template, g
import flask
import MySQLdb
from config import *
from db import *

app = Flask(__name__)

def getDb():
	global config
	conn = getattr(g, '_db', None)
	if conn is None:
		db = g._db = DB(host=config["host"], user=config["user"], password=config["password"], database=config["db"])
		db.connectDB()
	return db


@app.route('/')
def main():
	return render_template("main.html")

@app.route('/monsters')
def getMonsters():
	conn = None
	conn = getDb()
	query = """
			SELECT 	m.monster_id, 
					m.name, 
					m.desc,
					md.drop_one, 
					md.drop_two, 
					md.drop_three 
			FROM monster as m
			join monster_drop as md 
				on md.monster_id = m.monster_id
			order by m.desc, m.name
	"""

	results = conn.select(query)
	newResult = []
	for result in results:
		newResult.append({
			"monster_id": str(result[0]).replace("u", "").replace("\'", "").replace("\"", "").encode("utf-8"),
			"name": str(result[1]).replace("u", "").replace("\'", "").replace("\"", "").encode("utf-8"),
			"desc": str(result[2]).replace("u", "").replace("\'", "").replace("\"", "").encode("utf-8"),
			"drop_one_probability": str(result[3]).replace("u", "").replace("\'", "").replace("\"", "").encode("utf-8"),
			"drop_two_probability": str(result[4]).replace("u", "").replace("\'", "").replace("\"", "").encode("utf-8"),
			"drop_three_probability": str(result[5].replace("u", "").replace("\'", "").replace("\"", "").encode("utf-8"))
		})

	return flask.jsonify(newResult)

@app.route('/manuals/<monsterId>')
def getManuals(monsterId):
	conn = None
	conn = getDb()
	query = """
		SELECT 	manual.name,
				manual.manual_id,
				drop_table.drop_tier,
				drop_table.probability
		FROM drop_table 
		join manual 
			on manual.manual_id = drop_table.manual_id 
		WHERE monster_id = %s 
		AND manual.manual_id is not null
		order by manual.name
	"""

	results = conn.select(query, [str(monsterId)])
	newResult = []
	for result in results:
		newResult.append({
			"name": str(result[0]).replace("u", "").replace("\'", "").replace("\"", "").encode("utf-8"),
			"manual_id": str(result[1]).replace("u", "").replace("\'", "").replace("\"", "").encode("utf-8"),
			"drop_tier": str(result[2]).replace("u", "").replace("\'", "").replace("\"", "").encode("utf-8"),
			"probability": str(result[3]).replace("u", "").replace("\'", "").replace("\"", "").encode("utf-8")
		})
	return flask.jsonify(newResult)

@app.route('/items/<monsterId>')
def getItems(monsterId):
	conn = None
	conn = getDb()
	query = """
		SELECT 	item.name,
				item.item_id,
				drop_table.drop_tier,
				drop_table.probability
		FROM drop_table 
		join item 
			on item.item_id = drop_table.item_id 
		WHERE monster_id = %s 
		and item.item_id is not null
		order by item.name
	"""

	results = conn.select(query, [str(monsterId)])
	newResult = []
	for result in results:
		newResult.append({
			"name": str(result[0]).replace("u", "").replace("\'", "").replace("\"", "").encode("utf-8"),
			"item_id": str(result[1]).replace("u", "").replace("\'", "").replace("\"", "").encode("utf-8"),
			"drop_tier": str(result[2]).replace("u", "").replace("\'", "").replace("\"", "").encode("utf-8"),
			"probability": str(result[3]).replace("u", "").replace("\'", "").replace("\"", "").encode("utf-8")
		})
	return flask.jsonify(newResult)

#@app.teardown_context
#def closeConnection(exception):
#	db = getattr(g, '_db', None)
#	if db is not None:
#		del db

if __name__ == "__main__":
	app.run()
