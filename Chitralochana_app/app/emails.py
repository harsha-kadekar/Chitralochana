###########################################################################################
# Name: emails.py
# Description: This file will have functions to send admin or maintainance emails to admin
# Reference: Flask Web Development book
# Date: 11/3/2016
###########################################################################################
from flask import render_template, current_app
from flask_mail import Message
from manage import manager
from . import mail
from threading import Thread


def send_email(to, subject, template, **kwargs):
    msg = Message(current_app.config['SOCIALBUZZ_MAIL_SUBJECT_PREFIX'] + subject, sender=current_app.config['SOCIALBUZZ_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    thr = Thread(target=send_async_email, args=[manager.app, msg])
    thr.start()
    return thr


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

