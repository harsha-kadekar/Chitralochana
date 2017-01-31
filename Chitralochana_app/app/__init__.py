#######################################################################################################################
# Name: __init__.py
# Description:
# Developer: Harsha Kadekar
# References: https://github.com/aidanknowles/TweetVibe/blob/master/app/__init__.py
# Update: 1st version - 6/5/2016
#######################################################################################################################
from flask import Flask, session
from flask_mongoengine import MongoEngine
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager
from config import config
from langprocessing import SentimentAnalyzer

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = MongoEngine()
rel_db = SQLAlchemy()
#socketIO = SocketIO()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


# app = Flask(__name__)

# Read the configuration file
# app.config.from_object('config')

# socketIO = SocketIO(app)


# init_globalvariables()
# db = MongoEngine(app)
# rel_db = SQLAlchemy(app)
#senana = None
senana = SentimentAnalyzer()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    rel_db.init_app(app)
    # socketIO.init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    login_manager.init_app(app)

    #TODO::Instead of training everytime we start the server, once train it and store it. Load the model everytime.
    senana.sentiment_analysis_training(app.config['TRAINING_TW_DATA_FOLDER'] + app.config['TRAINING_TW_SENTIMENT_FILE'])

    return app