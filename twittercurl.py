from twitter import *
import os
import sys, codecs, locale
import beebdb

# ok these should be in another file for security purposes, 
# but since this is just a quick app I'll leave them here
consumerKey = r'79n4haW1NMwcKHXTmZMNA'
consumerSecret = r'GVzu6iesVyBPrwH1VArtGYMpgdAxPVdSXCioWD7XoM'

class TwitterCurl:
	def __init__(self, userName, maxTweets, forcehistory):
		appCredentials = os.path.expanduser('~/.beebdb_credentials')
		if not os.path.exists(appCredentials):
			oauth_dance("TwitterCurl", consumerKey, consumerSecret,
						appCredentials)	

		oauthToken, oauthSecret = read_token_file(appCredentials)

		self.twitter = Twitter(auth=OAuth(
			oauthToken, oauthSecret, consumerKey, consumerSecret))
		self.bdb = beebdb.BeebDB("beeb.db")
			
		self.userID = self.bdb.getUserID(userName)
		if self.userID == -1:
			self.userID = self.getTwitterUserID(userName)
			self.bdb.addUser(self.userID, userName)
		lastTweetID = self.bdb.getLatestTweetID(userID = self.userID)

		# Now work with Twitter
		# we use the since_id flag with the most recently saved tweet ID to speed up request
		# this is a bit lame since an accidental save of 1 tweet will mean requesting more via the command line will not actually show anything up
		# can get around this by not including the since_id, but, i'm not sure really what the use cases are here :)
		# anyway I've added the 'forceHistory' flag if you want to force pulling down tweets older than the most recently saved one
		# duplicated won't be saved, but
		tweets = {}
		if forcehistory:
			tweets = self.twitter.statuses.user_timeline(screen_name=userName, count=maxTweets)
		else:
			tweets = self.twitter.statuses.user_timeline(screen_name=userName, count=maxTweets, since_id =lastTweetID)
		
		savedTweets = 0
		dupeTweets = 0
		for tweet in tweets:
			if self.bdb.addTweet(tweet['id'], self.userID, tweet['text']):
				savedTweets+= 1
			else:
				dupeTweets += 1
		print("Saved", savedTweets, "tweets to database")
		if dupeTweets:
			print (dupeTweets, "tweets already seen")
			
	def getTwitterUserID(self, userName):
		user = self.twitter.users.show(screen_name = userName)
		return user['id']
	
	
	
if __name__ == '__main__':
	if len(sys.argv) < 3:
		print("Usage: twittercurl.py <Twitter Handle> <max number of tweets to pull>")
	else:
		forcehistory = False
		userName = sys.argv[1]
		maxTweets = sys.argv[2]
		if len(sys.argv) == 4 and sys.argv[3] == "forceHistory":
			forcehistory = True
		TwitterCurl(userName, int(maxTweets), forcehistory)
		