#####################################################################################
# Name: errors.py
# Description: This file will have all functions related to error scenarios of the
#              website.
# References: Flask Web Development
# Date: 11/2/2016
#####################################################################################

from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500