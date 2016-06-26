#######################################################################################################################
# Name: __init__.py
# Description:
# Developer: Harsha Kadekar
# References: https://github.com/aidanknowles/TweetVibe/blob/master/app/__init__.py
# Update: 1st version - 6/5/2016
#######################################################################################################################
from flask import Flask
from flask_mongoengine import MongoEngine
from mongoengine import connect
from config import MONGODB_NAME, MONGODB_HOST, MONGODB_HOSTADDRESS, MONGODB_PASSWORD, MONGODB_PORT, MONGODB_USERNAME

app = Flask(__name__)
app.config.from_object('config')

# connect(MONGODB_NAME, host=MONGODB_HOST+MONGODB_USERNAME+":"+MONGODB_PASSWORD+"@"+MONGODB_HOSTADDRESS)

db = MongoEngine(app)

from app import views