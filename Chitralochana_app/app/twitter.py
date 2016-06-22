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
from relations import Tweet, Tweet_User, Twitter_Hashtag



def GetTweets(searchString):
    auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    listOftweets = []
    user2tweets = {}
    hashtag2tweets = {}

    searchTweets = [status for status in tweepy.Cursor(api.search, q=searchString).items(MAX_FETCH_TWEETS)]
    for tweet in searchTweets:
        tweet_message = tweet.text.encode("utf-8")
        tweet_userhandle = tweet.user.screen_name
        tweet_retweet_count = tweet.retweet_count
        tweet_createtime = tweet.created_at
        tweet_location = tweet.geo
        tweet_favoritecount = tweet.favorites_count

        oneTweet = Tweet(tweet_message, tweet_createtime, tweet_userhandle, tweet_retweet_count, tweet_favoritecount, tweet_location)
        listOftweets.append(oneTweet)

        if user2tweets.has_key(tweet_userhandle):
            user = user2tweets[tweet_userhandle]
            user.tweets.append(oneTweet)
        else:
            tweet_username = tweet.user.name
            tweet_user_no_of_likes = tweet.user.favorites_count
            tweet_user_no_of_followers = tweet.user.followers_count
            tweet_user_no_of_following = tweet.user.friends_count
            user = Tweet_User(tweet_userhandle, tweet_username, tweet_user_no_of_following, tweet_user_no_of_followers, tweet_user_no_of_likes, None)
            user2tweets.__setitem__(tweet_userhandle, user)

        tweet_words = tweet_message.split(' ')
        for word in tweet_words:
            if word[0] == '#':
                hashtag = word[1:].lower()
                if hashtag2tweets.has_key(hashtag):
                    hashtag = hashtag2tweets[hashtag]
                    hashtag.Tweets.append(oneTweet)

    return listOftweets
