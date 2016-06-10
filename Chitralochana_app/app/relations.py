#######################################################################################################################
# Name: relations.py
# Description: This file has all the relations between different objects
# Developer: Harsha
# Reference:
# Update: 1st version 6/9/2016
#######################################################################################################################

class Tweet(object):
    def __init__(self, message, time, userhandle, retweet, relike, location):
        self.tweet_message = message
        self.tweet_datetime = time
        self.tweet_userhandle = userhandle
        self.tweet_retweets = retweet
        self.tweet_relikes = relike
        self.tweet_location = location

    def __str__(self):
        str = self.tweet_userhandle + " tweeted that '" + self.tweet_message.__str__() + "' at " + self.tweet_datetime.__str__()

class Tweet_User(object):
    def __init__(self, userhandle, username, following, follower, likes, no_of_tweet):
        self.tweet_userhandle = userhandle
        self.tweet_username = username
        self.tweet_following = following
        self.tweet_follower = follower
        self.tweet_likes = likes
        self.no_of_tweets = no_of_tweet
        self.tweets = []

class Twitter_Hashtag(object):
    def __init__(self, retweets, likes, users):
        self.tweets = []
        self.no_of_retweets = retweets
        self.no_of_likes = likes
        self.no_of_users = users
        self.related_hashtags = []
