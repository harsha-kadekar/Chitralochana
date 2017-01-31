#######################################################################################################################
# Name: data_downloader.py
# Description: This file will have functions and classes related to downloading of tweets from twitter.
# References: -
# Date: 1/31/2017
#######################################################################################################################

from tweepy import OAuthHandler, API, Cursor, Stream
from tweepy.streaming import StreamListener
from mongoengine import connect
from flask import current_app
from .models import Tweet
import thread
import json
import datetime
import sys
from .twitter import twittermetamodelBuilding
from .languageprocessing import LanguageProcessor
from .global_variables import user_searches_ongoing, TWITTER_DATA_DOWNLOADER_THREAD_INDEX, META_MODEL_BUILDER_THREAD_INDEX


class TweetListener(StreamListener):
    '''
    This class will be used to tune into twitter live stream. Each time a new tweet is recieved,
    it will parse the data recieved and store it in  the mongodb
    '''

    def __init__(self, api=None):
        self.num_tweets = 0
        self.max_tweets = 0
        self.user_id = None

    def on_data(self, feed):

        try:
            if feed != []:
                tweet = json.loads(feed)

                tweet_id = tweet['id']
                tweet_message = tweet['text'].encode("utf-8")
                tweet_userhandle = tweet['user']['screen_name']
                tweet_retweet_count = tweet['retweet_count']
                tweet_createtime = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')

                tweet_location = None
                tweet_geo = None
                tweet_favoritecount = tweet['favorite_count']
                tweet_username = tweet['user']['name']
                tweet_user_no_of_following = tweet['user']['friends_count']
                tweet_user_no_of_followers = tweet['user']['followers_count']
                tweet_positiveOrnegative = 0
                tweet_polarOrneutral = 0
                tweet_isRetweet = 0

                userSearchObj = user_searches_ongoing[self.user_id]

                try:

                    oneTweet = Tweet(tweet_id=tweet_id, tweet_msg=tweet_message, tweet_likes=tweet_favoritecount,
                                     tweet_retweets=tweet_retweet_count, tweet_search_category=None,
                                     tweet_user_search_query=userSearchObj.user_search_sentence, tweet_positiveOrnegative=tweet_positiveOrnegative,
                                     tweet_polarOrneutral=tweet_polarOrneutral, tweet_user_handle=tweet_userhandle,
                                     tweet_user_name=tweet_username, tweet_user_followers=tweet_user_no_of_followers,
                                     tweet_user_following=tweet_user_no_of_following, tweet_isretweet=tweet_isRetweet,
                                     tweet_time=tweet_createtime, tweet_location=tweet_location, tweet_geo=tweet_geo, tweet_search_userid=self.user_id)

                    oneTweet.save()
                except Exception as inst:
                    print inst.args
                    print inst.message
                    #print inst.
                if userSearchObj.threads_in_use[META_MODEL_BUILDER_THREAD_INDEX] is None:
                    print 'starting metamodel building'
                    userSearchObj.threads_in_use[META_MODEL_BUILDER_THREAD_INDEX] = thread.start_new_thread(twittermetamodelBuilding, (self.user_id,))

                self.num_tweets += 1

                if self.num_tweets < self.max_tweets:
                    return True
                else:
                    print 'completed tweet fetch'
                    userSearchObj.tweet_fetch_complete = True
                    return False
            else:
                return True
        except:
            print 'Unexpected error', sys.exc_info()[0]

        return True

    def on_error(self, status_code):
        print status_code
        pass


class DataDownloaderMethods(object):
    @staticmethod
    def twitterdownloadInitiator(user_id):
        '''
        This function will be used for initial analysis of the given user sentence.
        Then once initialized, it will start the thread which will download the tweets.
        :param user_sentence: Sentence or word provided by user to analyze
        :return: -
        '''

        userSearchObj = user_searches_ongoing[user_id]

        imp_words = LanguageProcessor.GetImportantWordsFromSentence(userSearchObj.user_search_sentence)

        if userSearchObj.realtime_search is False:
            userSearchObj.threads_in_use[TWITTER_DATA_DOWNLOADER_THREAD_INDEX] = thread.start_new_thread(DataDownloaderMethods.GetPastTweets, (user_id, imp_words, ))
        else:
            userSearchObj.threads_in_use[TWITTER_DATA_DOWNLOADER_THREAD_INDEX] = thread.start_new_thread(DataDownloaderMethods.GetCurrentTweets, (user_id, imp_words, ))


    @staticmethod
    def GetPastTweets(user_id, searchStrings):

        userSearchObj = user_searches_ongoing[user_id]

        auth = OAuthHandler( userSearchObj.configuration_parameters['consumer_key'], userSearchObj.configuration_parameters['consumer_secret'])
        auth.set_access_token(userSearchObj.configuration_parameters['access_token'], userSearchObj.configuration_parameters['access_token_secret'])
        api = API(auth)

        deleteEntries = connect(userSearchObj.configuration_parameters['mongodb']['DB'])
        deleteEntries.drop_database(userSearchObj.configuration_parameters['mongodb']['DB'])

        listTweetIDs = []

        user_query = userSearchObj.user_search_sentence

        userSearchObj.tweet_fetch_complete = False
        userSearchObj.meta_model_complete = False

        for searchString in searchStrings:
            # Sleep for 28 secs to avoid Twitter download rate restrictions
            searchTweets = [status for status in Cursor(api.search, q=searchString).items(userSearchObj.configuration_parameters['max_fetch_tweets'])]

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
                if userSearchObj.threads_in_use[META_MODEL_BUILDER_THREAD_INDEX] is None:
                    userSearchObj.threads_in_use[META_MODEL_BUILDER_THREAD_INDEX] = thread.start_new_thread(twittermetamodelBuilding, (user_id,))

        print 'completed tweet fetch'
        userSearchObj.tweet_fetch_complete = True
        pass

    @staticmethod
    def GetCurrentTweets(user_id, searchStrings):
        '''
        This function will help to fetch the tweets in real time. It is using twitter streaming apis
        :param searchStrings: List of keywords to be used for fetching tweets
        :return: -
        '''

        userSearchObj = user_searches_ongoing[user_id]

        print 'starting authentication twitter'
        auth = OAuthHandler(userSearchObj.configuration_parameters['consumer_key'], userSearchObj.configuration_parameters['consumer_secret'])
        auth.set_access_token(userSearchObj.configuration_parameters['access_token'], userSearchObj.configuration_parameters['access_token_secret'])
        lisNer = TweetListener()
        lisNer.user_id = user_id
        lisNer.max_tweets = userSearchObj.configuration_parameters['max_live_tweets']
        tweetStream = Stream(auth, lisNer)

        print 'mongodb settings now'

        deleteEntries = connect(userSearchObj.configuration_parameters['mongodb']['DB'])
        deleteEntries.drop_database(userSearchObj.configuration_parameters['mongodb']['DB'])

        print 'before session getcurrenttweets'

        userSearchObj.tweet_fetch_complete = False
        userSearchObj.meta_model_complete = False

        print 'after session getcurrenttweets'

        tweetStream.filter(track=searchStrings)

        pass
