##########################################################################################
# Name: app\auth\__init__.py
# Description: This file holds the functions related to initialization of authentication
#               blueprint.
# Reference: -
# Date: 1/30/2017
##########################################################################################

from flask import Blueprint

auth = Blueprint('auth',__name__)

from . import views