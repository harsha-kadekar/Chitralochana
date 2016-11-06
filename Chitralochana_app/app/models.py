#######################################################################################################################
# Name: models.py
# Description: This the file containing the description of the data which will be stored in the Mongodb
# Developer: Harsha
# Reference: https://github.com/aidanknowles/TweetVibe/blob/master/app/models.py
# Update: 1st Version 6/26/2015
#######################################################################################################################
from app import db, rel_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import login_manager

# This class represents the twitter data. Each object of this class represents one tweet.
class Tweet(db.Document):
    tweet_search_id = db.IntField(required=True)
    tweet_id = db.IntField(required=True, unique=True)
    tweet_msg = db.StringField()
    tweet_likes = db.IntField()
    tweet_retweets = db.IntField()
    tweet_search_category = db.StringField()
    tweet_user_search_query = db.StringField()
    tweet_positiveOrnegative = db.IntField()
    tweet_polarOrneutral = db.IntField()
    tweet_user_handle = db.StringField()
    tweet_user_name = db.StringField()
    tweet_user_followers = db.IntField()
    tweet_user_following = db.IntField()
    tweet_isretweet = db.IntField()
    tweet_time = db.DateTimeField()
    tweet_geo = db.DictField()
    tweet_location = db.StringField()


class User(UserMixin, rel_db.Model):
    __tablename__='user'
    userid = rel_db.Column(rel_db.Integer, primary_key=True)
    username = rel_db.Column(rel_db.String(64), index=True, unique=True)
    email = rel_db.Column(rel_db.String(64), index=True, unique=True)
    password_hash = rel_db.Column(rel_db.String(128))
    searches = rel_db.relationship('User_Searches', backref='user', lazy='dynamic')
    confirmed = rel_db.Column(rel_db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def get_id(self):
        return self.userid

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.userid})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.userid:
            return False
        self.confirmed = True
        rel_db.session.add(self)
        return True

class User_Searches(rel_db.Model):
    __tablename__= 'user_searches'
    searchid = rel_db.Column(rel_db.Integer, primary_key=True)
    user_id = rel_db.Column(rel_db.Integer, rel_db.ForeignKey('user.userid'))
    search_query = rel_db.Column(rel_db.String(120), index=True)
    search_realtime = rel_db.Column(rel_db.Boolean)
    search_date = rel_db.Column(rel_db.DateTime)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
