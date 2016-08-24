#######################################################################################################################
# Name: forms.py
# Description: This file has all the functions which creates different forms needed by the app
# Developer: Harsha
# Reference:
# Update: 1st version 6/5/2016
#######################################################################################################################
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

# This class represents the initial form displayed in the index page.
# It collects the user information from user.
class SearchForm(Form):
    user_input_string = StringField('user_input_string', validators=[DataRequired()])

