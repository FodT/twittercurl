import sqlite3

class BeebDB:

	def __init__(self, dbName):
		self.conn = sqlite3.connect(dbName)
		self.c = self.conn.cursor()
		#Create tables if needed
		# keep it super simple. one table for tweets, one table for users.
		with self.conn:
			self.conn.execute('''create table if not exists users
						(id int primary key, username text)''')
			self.conn.execute('''create table if not exists tweets
						(id int primary key, user_id int, tweet text)''')

	def __del__(self):
		self.conn.commit()
		self.c.close()
		
	def addUser(self, userID, userName):
		result = True
		row = [userID, userName]
		try:
			self.c.execute("INSERT INTO users VALUES (?, ?)", row)
		except:
			result = False
		self.conn.commit()
		return result
						
	def addTweet(self, tweetID, userID, tweetContent):
		result = True
		row = [tweetID, userID, tweetContent]
		try:
			self.c.execute("INSERT INTO tweets VALUES (?,?,?)", row)
		except:
			result = False
		self.conn.commit()
		return result
		
	def getUserID(self, userName):
		result = -1
		sql = """SELECT id FROM users WHERE username = '""" + userName +"""'"""
		self.c.execute(sql)
		row = self.c.fetchone()
		if row is not None:
			result = row[0]
		return result	
		
	def getLatestTweetID(self, userName="", userID=""):
		# either search for the user ID or the userName depending on which is specified.
		result = 1
		if not userID:
			userID = self.getUserID(userName)
		sql = """SELECT id FROM tweets where user_id = '""" + str(userID) + """' ORDER BY id DESC"""
		self.c.execute(sql)
		row = self.c.fetchone()
		if row is not None:
			result = row[0]
		return result
			