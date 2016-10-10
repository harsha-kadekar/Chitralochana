#######################################################################################################################
# Name: __init__.py
# Description:
# Developer: Harsha Kadekar
# References: https://github.com/aidanknowles/TweetVibe/blob/master/app/__init__.py
# Update: 1st version - 6/5/2016
#######################################################################################################################
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO
from globalvars import init_globalvariables
from langprocessing import SentimentAnalyzer

app = Flask(__name__)

# Read the configuration file
app.config.from_object('config')

socketIO = SocketIO(app)
# connect(MONGODB_NAME, host=MONGODB_HOST+MONGODB_USERNAME+":"+MONGODB_PASSWORD+"@"+MONGODB_HOSTADDRESS)

init_globalvariables()
db = MongoEngine(app)
#senana = None
senana = SentimentAnalyzer()
senana.sentiment_analysis_training()

from app import views