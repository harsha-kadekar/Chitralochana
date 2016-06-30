#######################################################################################################################
# Name: run_debug.py
# Description:
# Developer: Harsha Kadekar
# References:
# Updates: 1st Version - 6/5/2016
#######################################################################################################################
from app import app, socketIO

socketIO.run(app, debug=True)