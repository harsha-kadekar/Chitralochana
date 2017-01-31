######################################################################################
# Name: app\main\errors.py
# Description: This file will have all the different error handlers for the
#               application. Basically website error scenarios like 404, 500, etc
# References: -
# Date: 1/29/2017
######################################################################################

from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500