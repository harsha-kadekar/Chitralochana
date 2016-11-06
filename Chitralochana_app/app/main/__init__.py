#####################################################################################
# Name: __init__.py
# Description: This file provides the blueprint of the application.
# Reference: Flask Web Development book
# Date: 11/2/2016
######################################################################################

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors