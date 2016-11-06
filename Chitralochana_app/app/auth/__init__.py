#######################################################################################
# Name: __init__.py
# Description: This file has functions related to authentication blueprint. Basically
#              it initializes this blueprint
# References: Flask Web Development
# Date: 11/3/2016
########################################################################################

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views