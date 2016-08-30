#######################################################################################################################
# Name: relations.py
# Description: This file has all the relations between different objects using classes of models.py
# Developer: Harsha
# Reference:
# Update: 1st version 6/9/2016
#######################################################################################################################

# This class represents a twitter user. All the information will be extracted from the fetched tweets.
class Tweet_User(object):
    def __init__(self, userhandle, username, following, follower, likes, no_of_tweet, positiveCount, negativeCount, polarCount, neutralCount):
        self.tweet_userhandle = userhandle  # This is the twitter user handle ex @kadekar_harsha
        self.tweet_username = username      # This is the username used in the Twitter Harsha Kadekar
        self.tweet_following = following    # Number of twitter accounts user is following
        self.tweet_follower = follower      # Number of other twitter accounts which are following this account
        self.tweet_likes = likes            # Total number of likes of all the tweets
        self.no_of_tweets = no_of_tweet     # Total number of tweets user has tweeted
        self.positiveCount = positiveCount  # Total number of tweets having a positive tilt
        self.negativeCount = negativeCount  # Total number of tweets having a negative tilt
        self.polarCount = polarCount        # Total number of tweets having polarity
        self.neutralCount = neutralCount    # Total number of tweets which are neutral
        self.tweets = []                    # Tweets which are tweeted by the user
        self.hashtagsUsed = {}              # List of hashtags used by the user

# This class represent a twitter hashtag.
class Twitter_Hashtag(object):
    def __init__(self, hashtag_name, retweets, likes, users, negCount, posCount, neuCount, polCount):
        self.hash_tag = hashtag_name    # Name of the hashtag
        self.tweets = []                # tweets in which this hashtag is used
        self.no_of_retweets = retweets  # Total retweets count of the tweets of this hashtag
        self.no_of_likes = likes        # Total likes/favorites of the tweets of this hashtag
        self.no_of_users = users        # Total number of users using this hashtag
        self.negativecount = negCount   # Number of tweets having negative sentiment
        self.positiveCount = posCount   # Number of tweets having positive sentiment
        self.polarityCount = polCount   # Number of tweets which are polar
        self.neutralCount = neuCount    # Number of tweets which are neutral
        self.related_hashtags = {}      # All the hashtags used along with this hashtags
