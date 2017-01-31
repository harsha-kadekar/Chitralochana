#######################################################################################################################
# Name: views.py
# Description: This is python-flask view section. Here all the webpages has its own corresponding functions.
# Developer: Harsha Kadekar
# References:
# Update: 1st version - 6/5/2016
#######################################################################################################################
# from app import app, socketIO
from flask import render_template, flash, redirect, url_for, request, session, current_app
from flask_login import login_required
from . import main
from .forms import SearchForm
from .. import db, rel_db
from ..models import User
from ..DataDownloader import DataDownloaderMethods
import thread



# This is the main page of the website where user provides the search string.
# Once it validates the form, it will create the language processing thread and it will pass the user sentence to it.
# Then redirects or move to analyze page.
@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if session.__contains__('initialize') == False:
        session['userSentence'] = None
        session['tweetThread'] = None
        session['metamodelThread'] = None
        session['languageProcessingThread'] = None
        session['completeTweetFetch'] = False
        session['completedMetaModel'] = False
        session['realtime'] = True
        session['initialize'] = True
    form = SearchForm()
    if form.validate_on_submit():
        flash("User input = '" + form.user_input_string.data +"' will be analyzed ")
        print form.user_input_string.data
        session['usersentence'] = form.user_input_string.data.__str__()
        session['realtime'] = bool(form.realtime.data.__str__())

        myapp = current_app._get_current_object()


        session['languageProcessingThread'] = thread.start_new_thread(DataDownloaderMethods.twitterdownloadInitiator,(myapp, session['usersentence'], session['realtime'],))
        return redirect(url_for('.analyze'))

    return render_template('index.html', title='Home', form=form)

# This is the function which will be called when a client/browser wants to connect to the server using websocket.
# This is actually responding to connect events of browsers websocket.
#@socketIO.on('connect', namespace='/analyze')
#def connect_analyze():
#    print 'Connect Signal'

# This function will respond to any requests made by the client browsers response event websocket.
# In our case this will not happen as only from server data will be sent to client.
#@socketIO.on('response event', namespace='/analyze')
#def response_events(data):
#    print 'response event'
#    print data

# This function corresponds to analyze page. Actually here inside the page or UI of the page doesnot do any analysis.
# All the analysis will be done at the backend and only results will be showed in this page. It is a live page
# which will get update every few seconds using websockets
@main.route('/analyze')
@login_required
def analyze():
    sentence = session['usersentence']
    return render_template('analyze.html', title=sentence, userquerysearch=sentence)
