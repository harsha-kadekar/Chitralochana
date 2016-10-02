#######################################################################################################################
# Name: config.py
# Description: This file has all the configuration parameters used by this app.
# Reference:
# Update: 1st Version - 6/5/2016
#######################################################################################################################
import os

# Folder where the application or website is residing
basedir = os.path.abspath(os.path.dirname(__file__))

# To check cross scripting in python flask.
WTF_CSRF_ENABLED = True
# For cross scripting avoiding python flask will use this key
SECRET_KEY = 'Xtra1Care&For5Special&Key!2'

# Configuration related to MONGODB configuration
MONGODB_NAME = 'Tweetsdb'
MONGODB_HOST = ''
MONGODB_HOSTADDRESS = ''
MONGODB_PORT = ''
MONGODB_USERNAME = ''
MONGODB_PASSWORD = ''
MONGODB_SETTINGS = {'DB': "tweetDB"}

# Emails of site administrators
ADMINS = [
    'harsha.kadekar@gmail.com'
]

# Twitter APP Keys
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''
TWITTER_ACCESS_TOKEN = ''
TWITTER_ACCESS_TOKEN_SECRET = ''

# Keys related to Tweet fetch
MAX_FETCH_TWEETS = 100
MAX_LIVE_TWEETS = 1000

# Keys related to metamodel building
MAX_WORD_COUNTS = 200   # In case of word cloud, top number of words with most frequency

# Facebook APP keys
FACEBOOK_APP_ID = ''
FACEBOOK_SECRET_KEY = ''

TRAINING_TW_DATA_FOLDER = 'C:\\D_Drive\\Experiments\\NLP\\Twitter\\'
TRAINING_TW_SENTIMENT_FILE = 'sentiment.data'

