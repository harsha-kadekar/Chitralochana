#######################################################################################################################
# Name: DataDownloader
# Description: This file will hold functions and classes which are needed for the downloading of data from internet
# References: http://adilmoujahid.com/posts/2014/07/twitter-analytics/
# Date: 8/23/2016
#######################################################################################################################

from tweepy import OAuthHandler, API, Cursor, Stream
from tweepy.streaming import StreamListener
#from config import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, MAX_FETCH_TWEETS, MONGODB_SETTINGS, MAX_LIVE_TWEETS
from mongoengine import connect
from models import Tweet
from flask import Flask, current_app, session, copy_current_request_context
# from main import main
import thread
# import globalvars
import json
import datetime
import sys
from twitter import twittermetamodelBuilding
from langprocessing import LanguageProcessor



class TweetListener(StreamListener):
    '''
    This class will be used to tune into twitter live stream. Each time a new tweet is recieved,
    it will parse the data recieved and store it in  the mongodb
    '''

    def __init__(self, api=None):
        self.num_tweets = 0


    def on_data(self, feed):
        #print feed


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

                oneTweet = Tweet(tweet_id=tweet_id, tweet_msg=tweet_message, tweet_likes=tweet_favoritecount,
                                 tweet_retweets=tweet_retweet_count, tweet_search_category=None,
                                 tweet_user_search_query=session['userSentence'], tweet_positiveOrnegative=tweet_positiveOrnegative,
                                 tweet_polarOrneutral=tweet_polarOrneutral, tweet_user_handle=tweet_userhandle,
                                 tweet_user_name=tweet_username, tweet_user_followers=tweet_user_no_of_followers,
                                 tweet_user_following=tweet_user_no_of_following, tweet_isretweet=tweet_isRetweet,
                                 tweet_time=tweet_createtime, tweet_location=tweet_location, tweet_geo=tweet_geo)
                oneTweet.save()
                if session['metamodelThread'] is None:
                    print 'starting metamodel building'
                    session['metamodelThread'] = thread.start_new_thread(twittermetamodelBuilding, ())

                self.num_tweets += 1

                if self.num_tweets < current_app.config['MAX_LIVE_TWEETS']:
                    return True
                else:
                    print 'completed tweet fetch'
                    session['completeTweetFetch'] = True
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
    def twitterdownloadInitiator(app, user_sentence, realtime=False):
        '''
        This function will be used for initial analysis of the given user sentence.
        Then once initialized, it will start the thread which will download the tweets.
        :param user_sentence: Sentence or word provided by user to analyze
        :return: -
        '''

        with app.app_context():


            imp_words = LanguageProcessor.GetImportantWordsFromSentence(user_sentence)

            if realtime is False:
                session['tweetThread'] = thread.start_new_thread(DataDownloaderMethods.GetPastTweets, (app, imp_words, ))
            else:
                session['tweetThread'] = thread.start_new_thread(DataDownloaderMethods.GetCurrentTweets, (app, imp_words, ))


    @staticmethod
    def GetPastTweets(app, searchStrings):

        with app.app_context():

            auth = OAuthHandler( current_app.config['TWITTER_CONSUMER_KEY'], current_app.config['TWITTER_CONSUMER_SECRET'])
            auth.set_access_token(current_app.config['TWITTER_ACCESS_TOKEN'], current_app.config['TWITTER_ACCESS_TOKEN_SECRET'])
            api = API(auth)

            deleteEntries = connect(current_app.config['MONGODB_SETTINGS']['DB'])
            deleteEntries.drop_database(current_app.config['MONGODB_SETTINGS']['DB'])

            listTweetIDs = []

            user_query = session['userSentence']

            session['completeTweetFetch'] = False
            session['completedMetaModel'] = False

            for searchString in searchStrings:
                # Sleep for 28 secs to avoid Twitter download rate restrictions
                searchTweets = [status for status in Cursor(api.search, q=searchString).items(current_app.config['MAX_FETCH_TWEETS'])]

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
                    if session['metamodelThread'] is None:
                        session['metamodelThread'] = thread.start_new_thread(twittermetamodelBuilding, ())

            print 'completed tweet fetch'
            session['completeTweetFetch'] = True
        pass

    @staticmethod
    def GetCurrentTweets(app, searchStrings):
        '''
        This function will help to fetch the tweets in real time. It is using twitter streaming apis
        :param searchStrings: List of keywords to be used for fetching tweets
        :return: -
        '''



        print 'again testing let me check'

        with app.app_context():
            print 'starting authentication twitter'
            auth = OAuthHandler(current_app.config['TWITTER_CONSUMER_KEY'], current_app.config['TWITTER_CONSUMER_SECRET'])
            auth.set_access_token(current_app.config['TWITTER_ACCESS_TOKEN'], current_app.config['TWITTER_ACCESS_TOKEN_SECRET'])
            lisNer = TweetListener()
            tweetStream = Stream(auth, lisNer)


            print 'mongodb settings now'
            deleteEntries = connect(current_app.config['MONGODB_SETTINGS']['DB'])
            deleteEntries.drop_database(current_app.config['MONGODB_SETTINGS']['DB'])

            print 'before session getcurrenttweets'

            session['completeTweetFetch'] = False
            session['completedMetaModel'] = False

            print 'after session getcurrenttweets'

            tweetStream.filter(track=searchStrings)

        pass
