######################################################################################
# Name: app\main\views.py
# Description: This is the file which will handle all the different urls of the app.
# References: -
# Date: 1/29/2017
######################################################################################

from datetime import datetime
from flask import render_template, session, redirect, url_for, abort, flash, current_app
from flask_login import login_required, current_user
from thread import start_new_thread
from . import main
from .forms import SearchForm, EditProfileForm
from ..data_downloader import DataDownloaderMethods
from .. import db, socket_io
from ..models import User, Search
from ..global_variables import user_searches_ongoing, user_search_infosharing, USER_QUERY_WORD_EXTRACTOR_THREAD_INDEX, TWITTER_DATA_DOWNLOADER_THREAD_INDEX, META_MODEL_BUILDER_THREAD_INDEX


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """
    This function will handle the default http request to this website.
    In this it will handle the search form
    :return:
    """
    form = SearchForm()
    if form.validate_on_submit():
        session['userQuery'] = form.search.data
        session['realtime'] = form.realTime.data
        search = Search(search_item=form.search.data, realtime=form.realTime.data, timeOfSearch=datetime.utcnow(), user_id=current_user.id)
        db.session.add(search)
        infoSharingObj = None
        if user_searches_ongoing.has_key(current_user.id):
            infoSharingObj = user_searches_ongoing[current_user.id]
        else:
            infoSharingObj = user_search_infosharing(current_user.username, form.search.data, form.realTime.data)
            config_values = {}
            config_values.__setitem__('consumer_key', current_app.config['TWITTER_CONSUMER_KEY'])
            config_values.__setitem__('consumer_secret', current_app.config['TWITTER_CONSUMER_SECRET'])
            config_values.__setitem__('access_token', current_app.config['TWITTER_ACCESS_TOKEN'])
            config_values.__setitem__('access_token_secret', current_app.config['TWITTER_ACCESS_TOKEN_SECRET'])
            config_values.__setitem__('max_fetch_tweets', current_app.config['MAX_FETCH_TWEETS'])
            config_values.__setitem__('max_live_tweets', current_app.config['MAX_LIVE_TWEETS'])
            config_values.__setitem__('mongodb', current_app.config['MONGODB_SETTINGS'])
            config_values.__setitem__('max_words', current_app.config['MAX_WORD_COUNTS'])
            infoSharingObj.configuration_parameters = config_values
            user_searches_ongoing.__setitem__(current_user.id, infoSharingObj)

        infoSharingObj.threads_in_use[TWITTER_DATA_DOWNLOADER_THREAD_INDEX] = None
        infoSharingObj.threads_in_use[META_MODEL_BUILDER_THREAD_INDEX] = None
        infoSharingObj.tweet_fetch_complete = False
        infoSharingObj.meta_model_complete = False
        infoSharingObj.threads_in_use[USER_QUERY_WORD_EXTRACTOR_THREAD_INDEX] = start_new_thread(DataDownloaderMethods.twitterdownloadInitiator,(current_user.id,))

        return redirect(url_for('.analyze'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow())


@main.route('/user/<username>')
@login_required
def user(username):
    """
    This function handles the user profile view request.
    :param username: username of the user whose profile needs to be viewed.
    :return:
    """
    userView = User.query.filter_by(username=username).first()
    if userView is None:
        abort(404)
    return render_template('user.html', user=userView)

@main.route('/analyze')
@login_required
def analyze():
    """
    This will serve the analyze request from the user. Usually user will not give this request.
    As a result of search, this will be issued.
    :return:
    """
    print session.get('userQuery')
    return render_template('analyze.html', userquerysearch=session.get('userQuery'))


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.add(current_user)
        flash('Your profile has been updated')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.email.data = current_user.email
    form.username.data = current_user.username
    return render_template('edit_profile.html', form=form)


@socket_io.on('connect', namespace='/analyze')
def connect_analyze():
    """
    This is the function which will be called when a client/browser wants to connect to the server using websocket.
    This is actually responding to connect events of browsers websocket.
    :return:
    """
    print 'Connect Signal'


@socket_io.on('response event', namespace='/analyze')
def response_events(data):
    """
    This function will respond to any requests made by the client browsers response event websocket.
    In our case this will not happen as only from server data will be sent to client.
    :param data:
    :return:
    """
    print 'response event'
    print data




