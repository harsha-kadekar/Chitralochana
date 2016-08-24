#######################################################################################################################
# Name: models.py
# Description: This the file containing the description of the data which will be stored in the Mongodb
# Developer: Harsha
# Reference: https://github.com/aidanknowles/TweetVibe/blob/master/app/models.py
# Update: 1st Version 6/26/2015
#######################################################################################################################
from app import db

# This class represents the twitter data. Each object of this class represents one tweet.
class Tweet(db.Document):
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
