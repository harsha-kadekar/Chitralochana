#######################################################################################################################
# Name: globalvars
# Description: This file will have all the global variables used by this application
# References:
# Date: 8-23-2016
#######################################################################################################################

userSentence = ''
tweetThread = None
metamodelThread = None
languageProcessingThread = None
completeTweetFetch = False
completedMetaModel = False
realtime = False

def init_globalvariables():
    '''
    This function will initializes all the global variables.
    :return:
    '''
    global userSentence
    global tweetThread
    global metamodelThread
    global languageProcessingThread
    global completeTweetFetch
    global completedMetaModel
    global realtime

    userSentence = ''  # This will store the current user sentence which is being processed
    tweetThread = None  # This is the thread object which will fetch threads
    metamodelThread = None  # This is the thread which will build the metamodel based on the threats it has fetched.
    languageProcessingThread = None  # This is the thread where the language processing will take care. Language processing of user sentence and tweets
    completeTweetFetch = False  # This is to indicate that TweetFetchThread has completed the tweet fetching and putting in DB
    completedMetaModel = False  # This is to indicate that metamodel building is complete
    realtime = False            # This will tell whether the data needs to be pulled from live stream or from RESTful APIs