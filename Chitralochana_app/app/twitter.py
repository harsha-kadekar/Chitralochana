#######################################################################################################################
# Name: twitter.py
# Description: This file has functions to fetch tweets from Twitter
# Developer: Harsha
# Reference: https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
#            https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/
#            https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-3/
#            http://stats.seandolinar.com/collecting-twitter-data-using-a-python-stream-listener/
#            http://stackoverflow.com/questions/22469713/managing-tweepy-api-search
# Update: 1st Version 6/7/2015
#######################################################################################################################

from app import socketIO
from relations import Tweet_User, Twitter_Hashtag
from langprocessing import LanguageProcessor
from models import Tweet
import re
import time
from flask_socketio import emit
import json
import globalvars


def twittermetamodelBuilding():
    '''
    This function will be used to build the metamodel of the twitter data.
    This basically develops all the background data needed for the visualization, using Tweet data stored in DB.
    :return: -
    '''
    previouscount = 0

    while(True):

        if globalvars.completedMetaModel and globalvars.completeTweetFetch:
            time.sleep(2)
            continue

        print globalvars.userSentence, "From metamodel building"

        list_tweets = []
        user_tweets = {}
        hashtag_rel = {}
        list_tweets = Tweet.objects(tweet_user_search_query=globalvars.userSentence)
        tweet_msgs_lst = []

        no_of_retweets = 0
        no_of_likes = 0

        metadata = {}

        for tweet in list_tweets:
            new_user = False
            no_of_retweets += tweet.tweet_retweets
            no_of_likes += tweet.tweet_likes
            if user_tweets.has_key(tweet.tweet_user_handle):
                user = user_tweets[tweet.tweet_user_handle]
                user.tweet_likes += tweet.tweet_likes
                user.no_of_tweets += 1
            else:
                user = Tweet_User(tweet.tweet_user_handle, tweet.tweet_user_name, tweet.tweet_user_following, tweet.tweet_user_following, tweet.tweet_likes, 1, 0, 0, 0, 0)
                user_tweets.__setitem__(tweet.tweet_user_handle, user)
                new_user = True

            tweet_msgs_lst.append(tweet.tweet_msg)

            words = tweet.tweet_msg.split(' ')
            hashtags_lst = []
            for word in words:
                if word.__len__() > 1 and word[0] == '#':
                    hashtag_string = word[1:]
                    if not re.match("^[a-zA-Z0-9]*$", hashtag_string):
                        continue
                    hashtag_string = hashtag_string.lower()
                    if hashtag_rel.has_key(hashtag_string):
                        hashtag_obj = hashtag_rel[hashtag_string]
                        hashtag_obj.no_of_retweets += tweet.tweet_retweets
                        hashtag_obj.no_of_likes += tweet.tweet_likes
                        hashtag_obj.tweets.append(tweet)
                        if new_user:
                            hashtag_obj.no_of_users += 1
                    else:
                        hashtag_obj = Twitter_Hashtag(hashtag_string, tweet.tweet_retweets, tweet.tweet_likes, 1, 0, 0, 0, 0)
                        hashtag_obj.tweets.append(tweet)
                        hashtag_rel.__setitem__(hashtag_string, hashtag_obj)
                    if not hashtags_lst.__contains__(hashtag_string):
                        hashtags_lst.append(hashtag_string)

            # print hashtags_lst
            for hashtag in hashtags_lst:
                hashtag_obj = hashtag_rel[hashtag]
                for otherhashtag in hashtags_lst:
                    if otherhashtag == hashtag:
                        continue
                    if not hashtag_obj.related_hashtags.has_key(otherhashtag):
                        hashtag_obj.related_hashtags.__setitem__(otherhashtag, hashtag_rel[otherhashtag])

        full_hashtags = ''
        topfiveHashtags = []
        for hashtag in hashtag_rel.keys():
            # full_hashtags = full_hashtags + '#' + hashtag + ' '
            if topfiveHashtags.__len__() == 0:
                topfiveHashtags.append((hashtag, (hashtag_rel[hashtag].tweets.__len__(), hashtag_rel[hashtag].no_of_likes, 0)))
            else:
                bfound = False
                for i in range(0, topfiveHashtags.__len__()):
                    if topfiveHashtags[i][1][0] < hashtag_rel[hashtag].tweets.__len__():
                        topfiveHashtags.insert(i, (hashtag, (hashtag_rel[hashtag].tweets.__len__(), hashtag_rel[hashtag].no_of_likes, 0)))
                        bfound = True
                        break
                if not bfound:
                    topfiveHashtags.insert(topfiveHashtags.__len__(), (hashtag, (hashtag_rel[hashtag].tweets.__len__(), hashtag_rel[hashtag].no_of_likes, 0)))

                if topfiveHashtags.__len__() > 10:
                    topfiveHashtags.__delitem__(10)

        for data in topfiveHashtags:
            print data
            full_hashtags = full_hashtags + '#' + data[0] + ' '

        wordlist = LanguageProcessor.Get_Common_Words_Tweets(tweet_msgs_lst)
        print wordlist

        full_hashtags = full_hashtags[:full_hashtags.__len__()-1]

        metadata.__setitem__('TotalTweets', list_tweets.__len__())
        metadata.__setitem__('TotalRetweets', no_of_retweets)
        metadata.__setitem__('TotalLikes', no_of_likes)
        metadata.__setitem__('TotalUsers', user_tweets.__len__())
        metadata.__setitem__('Hashtags', full_hashtags)
        metadata.__setitem__('Top5Hashtags', topfiveHashtags)
        metadata.__setitem__('WordList', wordlist)

        value = json.dumps(metadata)

        # socketIO.emit('stats', value, '/analyze')
        # emit('stats', value)
        socketIO.emit('stats', value, namespace='/analyze')
        if globalvars.completeTweetFetch is True:
            print 'Acknowledging Tweet fetch is complete'

        if previouscount == list_tweets.__len__() and globalvars.completeTweetFetch is True:
            print 'meta model build is done'
            globalvars.completedMetaModel = True
        else:
            previouscount = list_tweets.__len__()
        time.sleep(2)

        # socketIO.send('stats', json.dumps(metadata), '/analyze')




