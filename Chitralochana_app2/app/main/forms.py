######################################################################################
# Name: app\main\forms.py
# Description: This file holds all the form classes. Each class is associated to a
#              form which will be used in our website
# Reference: -
# Date: 1/29/2017
######################################################################################

from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp
from ..models import User


class SearchForm(Form):
    """
    This is a dummy form. It will be used for testing purpose
    """
    search = StringField('Search Sentence', validators=[DataRequired(), Length(1, 128)])
    realTime = BooleanField('real time')
    submit = SubmitField('Submit')


class EditProfileForm(Form):
    """
    This class is responsible for editing the user profile.
    """
    name = StringField('Real name', validators=[Length(0, 128)])
    location = StringField('Location', validators=[Length(0, 128)])
    about_me = TextAreaField('About me')
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots, or underscores')])
    submit = SubmitField('Save')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


