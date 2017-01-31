######################################################################################
# Name: app\auth\views.py
# Description: This file will hold all the functions which will address the routes
#               related to authentication and login.
# References: -
# Date: 1/30/2017
######################################################################################

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .. import db
from .forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    This function handles the log-in request from the user.
    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid email or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """
    This function will be called to handle the logout request from the user.
    :return:
    """
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    This function handles the new user registration request from the user
    :return:
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        flash('You can now sign in')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.before_app_request
def before_request():
    """
    This is a hook to the request call. This function will be called
    before processing the user http request.
    :return:
    """
    if current_user.is_authenticated:
        current_user.ping()

