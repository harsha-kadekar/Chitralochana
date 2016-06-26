#######################################################################################################################
# Name: twitter.py
# Description: This file has functions to fetch tweets from Twitter
# Developer: Harsha
# Reference: https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
#            http://stats.seandolinar.com/collecting-twitter-data-using-a-python-stream-listener/
# Update: 1st Version 6/7/2015
#######################################################################################################################
import tweepy
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import os
import io
import time
from config import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, MAX_FETCH_TWEETS
from relations import Tweet_User, Twitter_Hashtag
from models import Tweet

class listener(StreamListener):

    def __int__(self, start_time, time_limit):
        self.time = start_time
        self.time_limit = time_limit
        self.tweet_data = []

    def on_data(self, data):
        save_file = open('raw_tweets.jason', 'a', encoding='utf-8')
        while(time.time() - self.time) < self.time_limit:
            try:
                self.tweet_data.append(data)

                return True
            except BaseException, e:
                print 'failed on data', str(e)
                time.sleep(5)
                pass
        save_file = open('raw_tweets.jason', 'w', encoding='utf-8')
        save_file.write(u'[\n')
        save_file.write(','.join(self.tweet_data))
        save_file.write(u'\n]')
        save_file.close()




def GetPastTweets(searchStrings, user_query):
    auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    listOftweets = []
    user2tweets = {}
    hashtag2tweets = {}

    listTweetIDs = []

    for searchString in searchStrings:
        print searchString
        searchTweets = [status for status in tweepy.Cursor(api.search, q=searchString).items(MAX_FETCH_TWEETS)]
        somefile = io.open('dump.txt', 'a', encoding='utf-8')
        dump = searchTweets.__str__().encode('utf-8')
        somefile.write(unicode(dump))
        somefile.close()
        for tweet in searchTweets:
            tweet_id = tweet.id
            if listTweetIDs.__contains__(tweet_id):
                continue
            if len(Tweet.objects(tweet_id=tweet_id)) > 1:
                continue
            tweet_message = tweet.text.encode("utf-8")
            tweet_userhandle = tweet.user.screen_name
            tweet_retweet_count = tweet.retweet_count
            tweet_createtime = tweet.created_at
            tweet_location = None
            tweet_geo = None
            tweet_favoritecount = tweet.favorite_count
            tweet_username = tweet.user.name
            tweet_user_no_of_following = tweet.user.friends_count
            tweet_user_no_of_followers = tweet.user.followers_count
            tweet_positiveOrnegative = 0
            tweet_polarOrneutral = 0
            tweet_isRetweet = 0

            oneTweet = Tweet(tweet_id=tweet_id, tweet_msg=tweet_message, tweet_likes=tweet_favoritecount, tweet_retweets=tweet_retweet_count, tweet_search_category=searchString, tweet_user_search_query=user_query, tweet_positiveOrnegative=tweet_positiveOrnegative, tweet_polarOrneutral=tweet_polarOrneutral, tweet_user_handle=tweet_userhandle, tweet_user_name=tweet_username, tweet_user_followers=tweet_user_no_of_followers, tweet_user_following=tweet_user_no_of_following, tweet_isretweet=tweet_isRetweet, tweet_time=tweet_createtime, tweet_location=tweet_location, tweet_geo=tweet_geo)
            oneTweet.save()
            listTweetIDs.append(tweet_id)
    return listOftweets

def GetPresentTweets(searchStrings):
    auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

    time_to_start = time.time()

    twitter_stream = Stream(auth, listener(time_to_start, 20))
    twitter_stream.filter(track=searchStrings)

