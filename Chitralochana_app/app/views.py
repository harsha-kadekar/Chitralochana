#######################################################################################################################
# Name: views.py
# Description:
# Developer: Harsha Kadekar
# References:
# Update: 1st version - 6/5/2016
#######################################################################################################################
from app import app, socketIO, userSentence, languageProcessingThread
from flask import render_template, flash, redirect, url_for, request, session
from forms import SearchForm
from langprocessing import userProcessingandTwitterdownloadInitiator
from twitter import GetPastTweets, metamodelBuilding
from models import Tweet
import thread
from facebookapi import GetPosts

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    global userSentence
    form = SearchForm()
    if form.validate_on_submit():
        flash("User input = '" + form.user_input_string.data +"' will be analyzed ")
        print form.user_input_string.data

        # langProc = LanguageProcessor()
        # langProc.UserSentence = form.user_input_string.data.__str__()

        session['usersentence'] = form.user_input_string.data.__str__()
        userSentence = form.user_input_string.data.__str__()
        user_sentence = userSentence
        languageProcessingThread = thread.start_new_thread(userProcessingandTwitterdownloadInitiator,(user_sentence, ))
        return redirect(url_for('analyze'))
        # return render_template('analyze.html', title=langProc.UserSentence, usersentence=langProc.UserSentence, words=imp_words)

    return render_template('index.html', title='Home', form=form)

@socketIO.on('connect', namespace='/analyze')
def connect_analyze():
    print 'Connect Signal'

@socketIO.on('response event', namespace='/analyze')
def response_events(data):
    print 'response event'
    print data
    # user_query = session['usersentence']
    # global metamodelThread
    # metamodelThread = thread.start_new_thread(metamodelBuilding, (user_query, ))

@app.route('/analyze')
def analyze():
    sentence = session['usersentence']

    #global tweetThread

    #tweetThread = thread.start_new_thread(GetPastTweets, (imp_words, sentence, ))

    return render_template('analyze.html', title=sentence, userquerysearch=sentence)
