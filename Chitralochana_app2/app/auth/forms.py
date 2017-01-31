######################################################################################
# Name: app\auth\forms.py
# Description: This file holds functions related to the forms to be used during
#               authentication process.
# References: -
# Date: 1/30/2017
######################################################################################

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Email, DataRequired, Length, EqualTo, Regexp
from ..models import User


class LoginForm(Form):
    """
    This is the initial sign in/login form for the user.
    """
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(Form):
    """
    This class is responsible for the registration of a new user. It represents the
    form's content needed for registration
    """
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('UserName', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscore')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        """
        This will check if user given email is already taken up by some other user
        :param field: user typed email
        :return: if exists then raise an exception
        """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        """
        This will check if user given name is already taken up by some other user
        :param field: user type username
        :return: if exists then raise an exception
        """
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')




