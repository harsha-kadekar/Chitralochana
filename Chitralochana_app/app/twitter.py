#######################################################################################################################
# Name: twitter.py
# Description: This file has functions to fetch tweets from Twitter
# Developer: Harsha
# Reference: https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
# Update: 1st Version 6/7/2015
#######################################################################################################################
import tweepy
from tweepy import OAuthHandler
from config import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, MAX_FETCH_TWEETS



def GetTweetsSimple(searchString):
    auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    searchTweets = [status for status in tweepy.Cursor(api.search, q=searchString).items(MAX_FETCH_TWEETS)]
    for tweet in searchTweets:
        print tweet.text.encode("utf-8")
    return searchTweets
