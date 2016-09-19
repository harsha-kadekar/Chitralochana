#######################################################################################################################
# Name: DataDownloader
# Description: This file will hold functions and classes which are needed for the downloading of data from internet
# References:
# Date: 8/23/2016
#######################################################################################################################

from tweepy import OAuthHandler, API, Cursor
from config import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, MAX_FETCH_TWEETS, MONGODB_SETTINGS
from mongoengine import connect
from models import Tweet
import thread
import globalvars
from twitter import twittermetamodelBuilding
from langprocessing import LanguageProcessor

class DataDownloaderMethods(object):
    @staticmethod
    def twitterdownloadInitiator(user_sentence):
        '''
        This function will be used for initial analysis of the given user sentence.
        Then once initialized, it will start the thread which will download the tweets.
        :param user_sentence: Sentence or word provided by user to analyze
        :return: -
        '''

        print user_sentence
        print globalvars.userSentence, "From tweet download initiator"
        imp_words = LanguageProcessor.GetImportantWordsFromSentence(user_sentence)

        globalvars.tweetThread = thread.start_new_thread(DataDownloaderMethods.GetPastTweets, (imp_words, ))

    @staticmethod
    def GetPastTweets(searchStrings):

        auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        api = API(auth)

        deleteEntries = connect(MONGODB_SETTINGS['DB'])
        deleteEntries.drop_database(MONGODB_SETTINGS['DB'])

        listTweetIDs = []

        user_query = globalvars.userSentence
        print globalvars.userSentence, 'From past tweets'

        globalvars.completeTweetFetch = False
        globalvars.completedMetaModel = False

        for searchString in searchStrings:
            # Sleep for 28 secs to avoid Twitter download rate restrictions
            searchTweets = [status for status in Cursor(api.search, q=searchString).items(MAX_FETCH_TWEETS)]

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
                if globalvars.metamodelThread is None:
                    globalvars.metamodelThread = thread.start_new_thread(twittermetamodelBuilding, ())

        print 'completed tweet fetch'
        globalvars.completeTweetFetch = True
        pass
