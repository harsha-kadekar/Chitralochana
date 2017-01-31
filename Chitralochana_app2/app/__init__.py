#####################################################################################
# Name: app\__init__.py
# Description: This is the application factory of our website. This creates all the
#               flask extensions which is used by the application. It also reads
#               configuration and then initializes the app to each of created
#               extensions.
# Reference:
# Date: 1/29/2017
#####################################################################################

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO
from config import config
from global_variables import init_globalvariables, twitter_access_token, twitter_access_token_secret, twitter_consumer_key, twitter_consumer_secret, twitter_max_fetch_tweets, twitter_max_live_tweets, mongodb_settings
from languageprocessing import SentimentAnalyzer

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
tw_db = MongoEngine()
login_manager = LoginManager()
socket_io = SocketIO()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

senana = SentimentAnalyzer()


def create_app(config_name):
    '''
    This function will create our application with configuration as
    specified by the config_name. It then initializes all the extensions
    :param config_name: Configuration object to be created and associated
                        to application
    :return: created application
    '''
    global twitter_consumer_key
    global twitter_consumer_secret
    global twitter_max_live_tweets
    global twitter_max_fetch_tweets
    global twitter_access_token_secret
    global twitter_access_token
    global mongodb_settings

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    tw_db.init_app(app)
    socket_io.init_app(app)

    init_globalvariables()
    twitter_max_live_tweets = app.config['MAX_LIVE_TWEETS']
    twitter_max_fetch_tweets = app.config['MAX_FETCH_TWEETS']
    twitter_consumer_secret = app.config['TWITTER_CONSUMER_SECRET']
    twitter_consumer_key = app.config['TWITTER_CONSUMER_KEY']
    twitter_access_token_secret = app.config['TWITTER_ACCESS_TOKEN_SECRET']
    twitter_access_token = app.config['TWITTER_ACCESS_TOKEN']
    mongodb_settings = app.config['MONGODB_SETTINGS']

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # TODO::Instead of training everytime we start the server, once train it and store it. Load the model everytime.
    senana.sentiment_analysis_training(app.config['TRAINING_TW_DATA_FOLDER'] + app.config['TRAINING_TW_SENTIMENT_FILE'])

    return app
