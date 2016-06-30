#######################################################################################################################
# Name: relations.py
# Description: This file has all the relations between different objects
# Developer: Harsha
# Reference:
# Update: 1st version 6/9/2016
#######################################################################################################################

class Tweet_User(object):
    def __init__(self, userhandle, username, following, follower, likes, no_of_tweet, positiveCount, negativeCount, polarCount, neutralCount):
        self.tweet_userhandle = userhandle
        self.tweet_username = username
        self.tweet_following = following
        self.tweet_follower = follower
        self.tweet_likes = likes
        self.no_of_tweets = no_of_tweet
        self.positiveCount = positiveCount
        self.negativeCount = negativeCount
        self.polarCount = polarCount
        self.neutralCount = neutralCount
        self.tweets = []

class Twitter_Hashtag(object):
    def __init__(self, hashtag_name, retweets, likes, users, negCount, posCount, neuCount, polCount):
        self.hash_tag = hashtag_name
        self.tweets = []
        self.no_of_retweets = retweets
        self.no_of_likes = likes
        self.no_of_users = users
        self.negativecount = negCount
        self.positiveCount = posCount
        self.polarityCount = polCount
        self.neutralCount = neuCount
        self.related_hashtags = {}
