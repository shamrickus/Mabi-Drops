from flask import Flask, render_template, g
import flask
import MySQLdb
from config import *

app = Flask(__name__)


class DB():
	def __init__(self, host=None, user=None, password=None, database=None):
		self.host = host
		self.user = user
		self.password = password
		self.database = database
		self.cur = None
		self.db = None

	def connectDB(self):
		self.db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)
		self.cur = self.db.cursor()

	def select(self, query, where = None):
		self.cur.execute(query, where)
		return self.cur.fetchall()

	def __del__(self):
		if self.db:
			self.db.close()


def getDb():
	global config
	conn = getattr(g, '_db', None)
	if conn is None:
		db = g._db = DB(host=config["host"], user=config["user"], password=config["password"], database=config["db"])
		db.connectDB()
		#db = g._db = DB(host, user, password, database)
	return db


@app.route('/')
def main():
#	flask.url_for('static', filename='main.css')
#	flask.url_for('static', filename='main.js')
	return render_template("main.html")

@app.route('/monsters')
def getMonsters():
	conn = None
	conn = getDb()
	return flask.jsonify(conn.select("Select * FROM monster"))

@app.route('/items/<monsterId>')
def getItems(monsterId):
	conn = None
	conn = getDb()
	query = "SELECT Item.name FROM `Drop Table` join Item on Item.item_id = `Drop Table`.item_id WHERE monster_id = %s and `Drop Table`.item_id is not null"
	return flask.jsonify(conn.select(query, [str(monsterId)]))

#@app.teardown_context
#def closeConnection(exception):
#	db = getattr(g, '_db', None)
#	if db is not None:
#		del db

if __name__ == "__main__":
	app.run()
