#######################################################################################################################
# Name: views.py
# Description:
# Developer: Harsha Kadekar
# References:
# Update: 1st version - 6/5/2016
#######################################################################################################################
from app import app
from flask import render_template, flash, redirect, url_for, request, session
from forms import SearchForm
from langprocessing import LanguageProcessor
from twitter import GetTweets
from facebookapi import GetPosts

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        flash("User input = '" + form.user_input_string.data +"' will be analyzed ")
        print form.user_input_string.data
        langProc = LanguageProcessor()
        langProc.UserSentence = form.user_input_string.data.__str__()
        imp_words = langProc.GetImportantWords()
        session['usersentence'] = langProc.UserSentence
        session['words'] = imp_words
        return redirect(url_for('analyze'))
        # return render_template('analyze.html', title=langProc.UserSentence, usersentence=langProc.UserSentence, words=imp_words)

    return render_template('index.html', title='Home', form=form)

@app.route('/analyze')
def analyze():
    sentence = session['usersentence']
    imp_words = session['words']
    for word in imp_words:
        # GetTweets(word)
        GetPosts(word)
    return render_template('analyze.html', title=sentence, usersentance=sentence, words=imp_words)
