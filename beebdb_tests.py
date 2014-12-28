import beebdb
import unittest
import sqlite3

class TestDBFunctions(unittest.TestCase):
	def setUp(self):
		self.BDB = beebdb.BeebDB('test.db')
		self.conn = sqlite3.connect('test.db')
		self.c = self.conn.cursor()

	def tearDown(self):
		self.BDB = None
		sql = """DELETE FROM 'users'"""
		self.c.execute(sql)
		self.conn.commit()
		sql = """DELETE FROM 'tweets'"""
		self.c.execute(sql)
		self.conn.commit()
		
	def test_tablesExist(self):
		usersql = """select count(type) from sqlite_master where type='table' and name='users'"""
		tweetsql = """select count(type) from sqlite_master where type='table' and name='tweets'"""
		self.c.execute(usersql)
		self.assertEqual(self.c.fetchone()[0], 1)
		self.c.execute(tweetsql)
		self.assertEqual(self.c.fetchone()[0], 1)
		
	def test_addUser(self):
		self.BDB.addUser(123456, "Fod")
		sql = """select * from users where username = 'Fod'"""
		self.c.execute(sql)
		row = self.c.fetchone()
		self.assertEqual(row[0], 123456)
		self.assertEqual(row[1], "Fod")
		
	def test_addSameUser(self):
		self.BDB.addUser(123456, "Fod")
		self.assertEqual(self.BDB.addUser(123456, "FodDupe"), False)
		
		
	def test_addTweet(self):
		self.BDB.addTweet(1, 123456, "Hello this is Fod")
		self.BDB.addTweet(2, 123456, "Hello this is Fod1")
		self.BDB.addTweet(3, 123456, "Hello this is Fod2")
		sql = """select * from tweets where user_id = 123456"""
		self.c.execute(sql)
		rows = self.c.fetchall()
		self.assertEqual(rows[0][0], 1)
		self.assertEqual(rows[0][1], 123456)
		self.assertEqual(rows[0][2], "Hello this is Fod")
		self.assertEqual(rows[1][0], 2)
		self.assertEqual(rows[1][1], 123456)
		self.assertEqual(rows[1][2], "Hello this is Fod1")
		self.assertEqual(rows[2][0], 3)
		self.assertEqual(rows[2][1], 123456)
		self.assertEqual(rows[2][2], "Hello this is Fod2")
		
	def test_addSameTweet(self):
		self.BDB.addTweet(1, 123456, "Hello this is Fod")
		self.assertEqual(self.BDB.addTweet(1, 123456, "Different tweet with same ID! Invalid"), False)
	
	def test_getUserID(self):
		self.BDB.addUser(123456, "Fod")
		id = self.BDB.getUserID("Fod")
		self.assertEqual(id, 123456)
	
	def test_getUserID_nonexistent(self):
		id = self.BDB.getUserID("IWontExist")
		self.assertEqual(id, -1)
		
	def test_getLastTweetID(self):
		self.BDB.addTweet(1, 123456, "Hello this is my first tweet")
		self.BDB.addTweet(4, 333333, "Hello this is someone completely different")
		self.BDB.addTweet(2, 123456, "Hello this is my latest tweet")
		id = self.BDB.getLatestTweetID(userID = 123456)
		
		sql = """select * from tweets"""
		self.c.execute(sql)
		rows = self.c.fetchall()
		self.assertEqual(id, 2)
		
	def test_getLastTweetID_no_tweets(self):
		id = self.BDB.getLatestTweetID(userID = 123456)
		self.assertEqual(id, 1)
		
		
	def test_getLastTweetIDFromUserName(self):
		self.BDB.addUser(123456, "Fod")
		self.BDB.addUser(333333, "SomeoneElse")
		self.BDB.addTweet(1, 123456, "Hello this is my first tweet")
		self.BDB.addTweet(4, 333333, "Hello this is someone completely different")
		self.BDB.addTweet(2, 123456, "Hello this is my latest tweet")
		id = self.BDB.getLatestTweetID(userName = "Fod")
		
		sql = """select * from tweets"""
		self.c.execute(sql)
		rows = self.c.fetchall()
		self.assertEqual(id, 2)
		
		
if __name__ == '__main__':
	unittest.main()