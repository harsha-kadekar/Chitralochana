#######################################################################################################################
# Name: global_variables.py
# Description: This file has all the global variables which will be used by the application.
# References: -
# Date: 1/30/2017
######################################################################################################################

user_searches_ongoing = {}

TWITTER_DATA_DOWNLOADER_THREAD_INDEX = 0
USER_QUERY_WORD_EXTRACTOR_THREAD_INDEX = 1
META_MODEL_BUILDER_THREAD_INDEX = 2

twitter_consumer_key = None
twitter_consumer_secret = None
twitter_access_token = None
twitter_access_token_secret = None
twitter_max_fetch_tweets = 0
twitter_max_live_tweets = 0
mongodb_settings = None


class user_search_infosharing(object):
    """
    This is the object which will be created when user first time logs in and gives first
    search string for the session. This class has all necessary information needed to
    execute complete functionality. Object will be put in the user_searches_ongoing dictionary
    along with the username as key. So every new search retrive from dictionary and modify
    contents
    """
    def __init__(self, username, searchquery, realtime):
        self.userName = username
        self.userSearchQuery = searchquery
        self.isSearchRealtime = realtime
        self.tweetFetchComplete = False
        self.metaModelComplete = False
        self.threadsExecuting = []
        self.configSettings = {}
        for i in xrange(0, 3):
            self.threadsExecuting.append(None)

    @property
    def user_name(self):
        return self.userName

    @user_name.setter
    def user_name(self, value):
        self.userName = value

    @property
    def user_search_sentence(self):
        return self.userSearchQuery

    @user_search_sentence.setter
    def user_search_sentence(self, value):
        self.userSearchQuery = value

    @property
    def realtime_search(self):
        return self.isSearchRealtime

    @realtime_search.setter
    def realtime_search(self, value):
        self.isSearchRealtime = value

    @property
    def threads_in_use(self):
        return self.threadsExecuting

    @threads_in_use.setter
    def threads_in_use(self, value):
        self.threadsExecuting = value

    @property
    def tweet_fetch_complete(self):
        return self.tweetFetchComplete

    @tweet_fetch_complete.setter
    def tweet_fetch_complete(self, value):
        self.tweetFetchComplete = value

    @property
    def meta_model_complete(self):
        return self.metaModelComplete

    @meta_model_complete.setter
    def meta_model_complete(self, value):
        self.metaModelComplete = value

    @property
    def configuration_parameters(self):
        return self.configSettings

    @configuration_parameters.setter
    def configuration_parameters(self, value):
        self.configSettings = value


def init_globalvariables():
    """
    This function initializes all the global variables used by the application
    :return: -
    """
    global user_searches_ongoing
    global TWITTER_DATA_DOWNLOADER_THREAD_INDEX
    global USER_QUERY_WORD_EXTRACTOR_THREAD_INDEX
    global META_MODEL_BUILDER_THREAD_INDEX

    global twitter_consumer_key
    global twitter_consumer_secret
    global twitter_access_token
    global twitter_access_token_secret
    global twitter_max_fetch_tweets
    global twitter_max_live_tweets
    global mongodb_settings

    twitter_consumer_key = None
    twitter_consumer_secret = None
    twitter_access_token = None
    twitter_access_token_secret = None
    twitter_max_fetch_tweets = 0
    twitter_max_live_tweets = 0
    mongodb_settings = None

    user_searches_ongoing = {}
    TWITTER_DATA_DOWNLOADER_THREAD_INDEX = 0
    USER_QUERY_WORD_EXTRACTOR_THREAD_INDEX = 1
    META_MODEL_BUILDER_THREAD_INDEX = 2