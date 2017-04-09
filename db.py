import MySQLdb


def reset(config):
	db = MySQLdb.connect(host=config["host"], user=config["user"], passwd=config["password"], db=config["db"])

	cur = db.cursor()

	with open('Drop-Table/db.sql', 'r') as file:
		data = file.read()

	cur.execute(data)

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