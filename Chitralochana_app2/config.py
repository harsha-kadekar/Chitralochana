######################################################################################
# Name: config.py
# Description: This file holds all the configuration information needed to run the
#               application. It included cofigurations for testing and development
# References: -
# Date: 1/29/2017
######################################################################################

import os

baseDir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    This is the base class which has configurations which are
    common to all types of configuration
    """
    # For cross scripting avoidance, python flask will use this
    SECRET_KEY = 'Xtra1Care&For5Special&Key!2'
    # To check cross scripting in python flask
    WTF_CSRF_ENABLED = True

    # Configurations related to SQL_ALCHEMY
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_MIGRATE_REPO = os.path.join(baseDir, 'db_repository')

    # Configurations related to mailing from the server
    SOCIAL_BUZZ_MAIL_SUBJECT_PREFIX = '[SocialBuzZzZz]'
    SOCIAL_BUZZ_MAIL_SENDER = 'Admin <socialbuzzzzz@example.com>'
    SOCIAL_BUZZ_MAIL_ADMIN = ['harsha.kadekar@gmail.com']

    # Twitter app related keys needed for authentication
    TWITTER_CONSUMER_KEY = ''
    TWITTER_CONSUMER_SECRET = ''
    TWITTER_ACCESS_TOKEN = ''
    TWITTER_ACCESS_TOKEN_SECRET = ''

    # Configs related to fetching of tweets
    MAX_FETCH_TWEETS = 100
    MAX_LIVE_TWEETS = 1000

    # Keys related to metamodel building
    MAX_WORD_COUNTS = 200  # In case of word cloud, top number of words with most frequency

    # settings related to machine learning, AI and NLP dataset
    TRAINING_TW_DATA_FOLDER = 'C:\\D_Drive\\Coding\\TestData\\Twitter\\'
    TRAINING_TW_SENTIMENT_FILE = 'sentiment.data'

    @staticmethod
    def init_app(app):
        pass


class developmentConfig(Config):
    """
    This class is very specific to development environment configuration.
    """
    DEBUG = True

    # settings related to mail configuration or smtp server
    MAIL_SERVER = ''
    MAIL_PORT = ''
    MAIL_USE_TLS = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''

    # settings related to relational db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(baseDir, 'data-dev.sqlite')

    # settings related to non relational db
    MONGODB_NAME = 'dev-tweetsdb'
    MONGODB_SETTINGS = {'DB': "dev-tweetsdb"}


class testingConfig(Config):
    """
    This class will hold configurations which are specific to testing environment
    """
    TESTING = True

    # settings related to relational db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(baseDir, 'data-test.sqlite')

    # settings related to non relational db
    MONGODB_NAME = 'test-tweetsdb'
    MONGODB_SETTINGS = {'DB': "test-tweetsdb"}


class productionConfig(Config):
    """
    This class will hold configurations which are specific to production environment
    """

    # settings related to relational db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(baseDir, 'data-test.sqlite')

    # settings related to non relational db
    MONGODB_NAME = 'tweetsdb'
    MONGODB_SETTINGS = {'DB': "tweetsdb"}


config = {
    'development': developmentConfig,
    'testing': testingConfig,
    'production': productionConfig,

    'default': developmentConfig
}
