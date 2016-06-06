#######################################################################################################################
# Name: views.py
# Description:
# Developer: Harsha Kadekar
# References:
# Update: 1st version - 6/5/2016
#######################################################################################################################
from app import app
from flask import render_template, flash, redirect, url_for
from forms import SearchForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        flash("User input = '" + form.user_input_string.data +"' will be analyzed ")
        return redirect(url_for('index'))

    return render_template('index.html', title='Home', form=form)