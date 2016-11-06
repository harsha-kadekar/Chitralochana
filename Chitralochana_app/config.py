#######################################################################################################################
# Name: config.py
# Description: This file has all the configuration parameters used by this app.
# Reference:
# Update: 1st Version - 6/5/2016
#######################################################################################################################
import os

# Folder where the application or website is residing
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    '''
    This class all the common configuration parameters needed to run this applicaiton.
    '''
    # To check cross scripting in python flask.
    WTF_CSRF_ENABLED = True
    # For cross scripting avoiding python flask will use this key
    SECRET_KEY = 'Xtra1Care&For5Special&Key!2'

    # Configuration related to SQL_ALCHEMY
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # Emails of site administrators
    ADMINS = [
        'harsha.kadekar@gmail.com'
    ]
    SOCIALBUZZ_MAIL_SUBJECT_PREFIX = '[SocialBuzzzzz]'
    SOCIALBUZZ_MAIL_SENDER = 'SOCIALBUZZ Admin <socialbuzz@example.com>'


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

    # Settings related to machine learning, NLP and AI data set
    TRAINING_TW_DATA_FOLDER = 'C:\\D_Drive\\Coding\\TestData\\Twitter\\' #'C:\\D_Drive\\Experiments\\NLP\\Twitter\\'
    TRAINING_TW_SENTIMENT_FILE = 'sentiment.data'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    '''
    This has specific configurations needed to run in development environment
    '''
    DEBUG = True

    # Settings related to mail configuration or smtp server
    MAIL_HOSTNAME = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = None
    MAIL_PASSWORD = None

    # Settings related to relational database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev-app.db')

    # Settings related to mongodb
    MONGODB_NAME = 'Dev-Tweetsdb'
    MONGODB_SETTINGS = {'DB': "Dev-tweetDB"}


class TestingConfig(Config):
    '''
    This has specific configurations needed to run in test environment
    '''
    Testing = True

    # Settings related to relational database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test-app.db')

    # Settings related to mongodb
    MONGODB_NAME = 'Test-Tweetsdb'
    MONGODB_SETTINGS = {'DB': "Test-tweetDB"}


class ProductionConfig(Config):
    '''
    This has specific configurations needed to run in production environment
    '''

    # Settings related to relational database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    # Settings related to mongodb
    MONGODB_NAME = 'Tweetsdb'
    MONGODB_SETTINGS = {'DB': "tweetDB"}

config = {
    'development':DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
