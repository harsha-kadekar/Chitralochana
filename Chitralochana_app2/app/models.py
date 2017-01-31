######################################################################################
# Name: models.py
# Description: This file all the classes corresponding to the relational entities
#               usually stored in the db
# References: -
# Date: 1/29/2017
######################################################################################

from . import db, login_manager, tw_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import request
from datetime import datetime
import hashlib


class Role(db.Model):
    """
    This class is dummy class. Usually each class represented here
    will have a respective table in the sqlite
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class Search(db.Model):
    """
    This class represent the search query done by a user
    """
    __tablename__ = 'searches'
    search_id = db.Column(db.Integer, primary_key=True)
    search_item = db.Column(db.String(128), index=True)
    realtime = db.Column(db.Boolean, default=False)
    timeOfSearch = db.Column(db.DateTime(), default=datetime.utcnow())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class User(UserMixin, db.Model):
    """
        This class is representation of the user. Usually each class represented here
        will have a respective table in the sqlite
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(128))
    location = db.Column(db.String(128))
    about_me = db.Column(db.Text())
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    searches = db.relationship('Search', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        This function verifies whether what user passed password is what
        stored in the db
        :param password: user passed password
        :return:
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    def ping(self):
        """
        This function is used to update the lastseen field.
        Everytime user sends request this function will be called
        :return:
        """
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar(self, size=100, default='identicon', rating='g'):
        """
        This function will help to get the gravatar profile pic for
        the email given by the user
        :param size:
        :param default:
        :param ratting:
        :return:
        """
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default, rating=rating)


class Tweet(tw_db.Document):
    """
    This class represent a tweet. This will be stored in the mongodb and not in sqllite
    """
    #tweet_search_id = tw_db.IntField(required=True)
    tweet_id = tw_db.IntField(required=True, unique=True)
    tweet_msg = tw_db.StringField()
    tweet_likes = tw_db.IntField()
    tweet_retweets = tw_db.IntField()
    tweet_search_category = tw_db.StringField()
    tweet_user_search_query = tw_db.StringField()
    tweet_positiveOrnegative = tw_db.IntField()
    tweet_polarOrneutral = tw_db.IntField()
    tweet_user_handle = tw_db.StringField()
    tweet_user_name = tw_db.StringField()
    tweet_user_followers = tw_db.IntField()
    tweet_user_following = tw_db.IntField()
    tweet_isretweet = tw_db.IntField()
    tweet_time = tw_db.DateTimeField()
    tweet_geo = tw_db.DictField()
    tweet_location = tw_db.StringField()
    tweet_search_userid = tw_db.IntField(required=True)


class Tweet_User(object):
    """
    This class represents a twitter user. All the information will be extracted from the fetched tweets.
    This will not be stored in db. It is only created and used in memory
    """
    def __init__(self, userhandle, username, following, follower, likes, no_of_retweet, positiveCount, negativeCount, polarCount, neutralCount):
        self.tweet_userhandle = userhandle  # This is the twitter user handle ex @kadekar_harsha
        self.tweet_username = username      # This is the username used in the Twitter Harsha Kadekar
        self.tweet_following = following    # Number of twitter accounts user is following
        self.tweet_follower = follower      # Number of other twitter accounts which are following this account
        self.tweet_likes = likes            # Total number of likes of all the tweets
        self.no_of_retweets = no_of_retweet     # Total number of retweets of user tweets
        self.positiveCount = positiveCount  # Total number of tweets having a positive tilt
        self.negativeCount = negativeCount  # Total number of tweets having a negative tilt
        self.polarCount = polarCount        # Total number of tweets having polarity
        self.neutralCount = neutralCount    # Total number of tweets which are neutral
        self.user_ranking = None            # This gives the overall ranking based on Number of people being followed, tweets, likes and retweets
        self.tweets = []                    # Tweets which are tweeted by the user
        self.hashtagsUsed = {}              # List of hashtags used by the user


class Twitter_Hashtag(object):
    """
    This class represent a twitter hashtag.
    This will not be stored in db. It is only created and used in memory
    """
    def __init__(self, hashtag_name, retweets, likes, users, posCount, negCount, polCount, neuCount):
        self.hash_tag = hashtag_name    # Name of the hashtag
        self.tweets = []                # tweets in which this hashtag is used
        self.no_of_retweets = retweets  # Total retweets count of the tweets of this hashtag
        self.no_of_likes = likes        # Total likes/favorites of the tweets of this hashtag
        self.no_of_users = users        # Total number of users using this hashtag
        self.negativeCount = negCount   # Number of tweets having negative sentiment
        self.positiveCount = posCount   # Number of tweets having positive sentiment
        self.polarityCount = polCount   # Number of tweets which are polar
        self.neutralCount = neuCount    # Number of tweets which are neutral
        self.hashtag_rank = None        # This gives the overall ranking for all the hashtags based on tweets, users, likes and retweets
        self.related_hashtags = {}      # All the hashtags used along with this hashtags


@login_manager.user_loader
def load_user(user_id):
    """
    This is a coll back function used to get the user by the
    login functionality
    :param user_id: an id indicating a particular user
    :return: user representing the user_id
    """
    return User.query.get(int(user_id))



