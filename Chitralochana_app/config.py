#######################################################################################################################
# Name: config.py
# Description: This file has all the configuration parameters used by this app.
# Reference:
# Update: 1st Version - 6/5/2016
#######################################################################################################################
import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'Xtra1Care&For5Special&Key!2'

ADMINS = [
    'harsha.kadekar@gmail.com'
]

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''
TWITTER_ACCESS_TOKEN = ''
TWITTER_ACCESS_TOKEN_SECRET = ''
MAX_FETCH_TWEETS = 10