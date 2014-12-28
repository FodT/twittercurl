Twittercurl: a quick and dirty twitter archive utility
requires Python 3.3 and the Python Twitter Tools (http://mike.verdone.ca/twitter/)

The tool saves the database using sqlite so the created files can be viewed using any freely available tool.

Usage: py twittercurl.py UserName MaxNoOfTweets [forceHistory]
e.g to pull the latest 10 tweets from @deftones:
>py twittercurl.py deftones 10

The app was tested in windows, I can't guarantee it will run on other platforms.
The first time the app is run, it will most likely request authentication from twitter. 
This is handled by the python twitter tools and you will be walked through the steps.

to speed up requests through the twitter API, twittercurl only requests the last X tweets onwards from the last saved tweet by that user.
To work around this, use the 'forceHistory' flag. e.g

>py twittercurl.py deftones 1
1 tweets saved

>py twittercurl.py deftones 2
0 tweets saved

>py twittercurl.py deftones 2 forceHistory
1 tweets saved
1 tweets seen before

I had set up a small test twitter account, @FotiosTest, to work with. About midway through development I realised it could be used to pull any users' tweets, so I extended it do so.
The database is very simple, storing user ids to screen names, and tweet ids to tweet contents along with the posting user id. 
It could be extended to contain more data and map more relationships (users to followers, retweets etc), but I was keeping it simple for the sake of the exercise.

the tool only downloads tweets from the specified user's timeline, not their 'home' timeline which includes retweets and tweets posted by that user's followers.

