######################################################################################
# Name: app\main\__init__.py
# Description: This is a blueprint. Means all the routes defined here are in dormant
#               state until it is associated with an application. This is useful when
#               we are creating application object in realtime.
# Reference: -
# Date: 1/29/2017
######################################################################################

from flask import Blueprint

main = Blueprint('main', __name__)

# moment we import these views and error handlers, automatically all the routes
# will be associated. So we are importing at the end after creation of main
# blueprint.
from . import views, errors