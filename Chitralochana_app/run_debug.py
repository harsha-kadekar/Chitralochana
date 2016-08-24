#######################################################################################################################
# Name: run_debug.py
# Description: This python script will be used host the python-flask website in a debug mode
# Developer: Harsha Kadekar
# References:
# Updates: 1st Version - 6/5/2016
#######################################################################################################################
from app import app, socketIO

socketIO.run(app, debug=True)