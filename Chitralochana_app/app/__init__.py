#######################################################################################################################
# Name: __init__.py
# Description:
# Developer: Harsha Kadekar
# References:
# Update: 1st version - 6/5/2016
#######################################################################################################################
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app import views