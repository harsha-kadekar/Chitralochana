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
                    if not user.hashtagsUsed.has_key(hashtag_string):
                        user.hashtagsUsed.__setitem__(hashtag_string, hashtag_obj)

            # print hashtags_lst
            for hashtag in hashtags_lst:
                hashtag_obj = hashtag_rel[hashtag]
                hashtag_obj.hashtag_rank = hashtag_rank_calculator(hashtag_obj.tweets.__len__(), hashtag_obj.no_of_users, hashtag_obj.no_of_retweets, hashtag_obj.no_of_likes)
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
                topfiveHashtags.append((hashtag, hashtag_rel[hashtag].hashtag_rank))
            else:
                bfound = False
                for i in range(0, topfiveHashtags.__len__()):
                    if topfiveHashtags[i][1] < hashtag_rel[hashtag].hashtag_rank:
                        topfiveHashtags.insert(i, (hashtag, hashtag_rel[hashtag].hashtag_rank))
                        bfound = True
                        break
                if not bfound:
                    topfiveHashtags.insert(topfiveHashtags.__len__(), (hashtag, hashtag_rel[hashtag].hashtag_rank))

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


def hashtag_rank_calculator(numTweets, numUsers, numRetweets, numLikes):
    '''
    This function will calculate a ranking for given hashtag.
    It each range of values a particular value will be given to parameters. Then total sum of parameter values gives the
    ranking.
    formula is Normalized(Number of tweets) + Normalized(Number of Users) + Normalized(Number of retweets) + Normalized(Number of likes)
    0-100: 0.1, 101-1000: 0.3, 1001-10000: 0.5, 10001-100000:0.7, 100001-1000000:0.9, 1000001-infi:1
    :param numTweets: Number of tweets which used this hashtag
    :param numUsers: Number of users who have used this users
    :param numRetweets: Total retweets done for this hashtag
    :param numLikes: Total number of likes present for this hashtag
    :return: Returns the rank of a hashtag
    '''

    normTweets = 0
    normUsers = 0
    normRetweets = 0
    normLikes = 0
    rank = 0

    if numTweets <= 100:
        normTweets = 0.1
    elif numTweets <= 1000:
        normTweets = 0.3
    elif numTweets <= 10000:
        normTweets = 0.5
    elif numTweets <= 100000:
        normTweets = 0.7
    elif numTweets <= 1000000:
        normTweets = 0.9
    else:
        normTweets = 1

    if numUsers <= 100:
        normUsers = 0.1
    elif numUsers <= 1000:
        normUsers = 0.3
    elif numUsers <= 10000:
        normUsers = 0.5
    elif numUsers <= 100000:
        normUsers = 0.7
    elif numUsers <= 1000000:
        normUsers = 0.9
    else:
        normUsers = 1

    if numLikes <= 100:
        normLikes = 0.1
    elif numLikes <= 1000:
        normLikes = 0.3
    elif numLikes <= 10000:
        normLikes = 0.5
    elif numLikes <= 100000:
        normLikes = 0.7
    elif numLikes <= 1000000:
        normLikes = 0.9
    else:
        normLikes = 1

    if numRetweets <= 100:
        normRetweets = 0.1
    elif numRetweets <= 1000:
        normRetweets = 0.3
    elif numRetweets <= 10000:
        normRetweets = 0.5
    elif numRetweets <= 100000:
        normRetweets = 0.7
    elif numRetweets <= 1000000:
        normRetweets = 0.9
    else:
        normRetweets = 1

    rank = normTweets + normUsers + normRetweets + normLikes
    rank = round(rank, 2)
    return rank




