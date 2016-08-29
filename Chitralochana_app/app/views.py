#######################################################################################################################
# Name: views.py
# Description: This is python-flask view section. Here all the webpages has its own corresponding functions.
# Developer: Harsha Kadekar
# References:
# Update: 1st version - 6/5/2016
#######################################################################################################################
from app import app, socketIO
from flask import render_template, flash, redirect, url_for, request, session
from forms import SearchForm
from DataDownloader import DataDownloaderMethods
import thread
import globalvars
from facebookapi import GetPosts

# This is the mail page of the website where user provides the search string.
# Once it validates the form, it will create the language processing thread and it will pass the user sentence to it.
# Then redirects or move to analyze page.
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        flash("User input = '" + form.user_input_string.data +"' will be analyzed ")
        print form.user_input_string.data
        session['usersentence'] = form.user_input_string.data.__str__()
        globalvars.userSentence = form.user_input_string.data.__str__()
        user_sentence = globalvars.userSentence
        print globalvars.userSentence
        globalvars.languageProcessingThread = thread.start_new_thread(DataDownloaderMethods.twitterdownloadInitiator,(user_sentence, ))
        return redirect(url_for('analyze'))

    return render_template('index.html', title='Home', form=form)

# This is the function which will be called when a client/browser wants to connect to the server using websocket.
# This is actually responding to connect events of browsers websocket.
@socketIO.on('connect', namespace='/analyze')
def connect_analyze():
    print 'Connect Signal'

# This function will respond to any requests made by the client browsers response event websocket.
# In our case this will not happen as only from server data will be sent to client.
@socketIO.on('response event', namespace='/analyze')
def response_events(data):
    print 'response event'
    print data

# This function corresponds to analyze page. Actually here inside the page or UI of the page doesnot do any analysis.
# All the analysis will be done at the backend and only results will be showed in this page. It is a live page
# which will get update every few seconds using websockets
@app.route('/analyze')
def analyze():
    sentence = session['usersentence']
    return render_template('analyze.html', title=sentence, userquerysearch=sentence)
