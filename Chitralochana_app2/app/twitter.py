#######################################################################################################################
# Name: twitter.py
# Description: This file has functions to fetch tweets from Twitter
# Developer: Harsha
# Reference: https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
#            https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/
#            https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-3/
#            http://stats.seandolinar.com/collecting-twitter-data-using-a-python-stream-listener/
#            http://stackoverflow.com/questions/22469713/managing-tweepy-api-search
# Update: 6/7/2016
#######################################################################################################################

from app import senana, socket_io
from languageprocessing import LanguageProcessor
from models import Tweet, Tweet_User, Twitter_Hashtag
import re
import time
from flask_socketio import emit
#from flask import current_app, session
from .global_variables import user_searches_ongoing, TWITTER_DATA_DOWNLOADER_THREAD_INDEX, META_MODEL_BUILDER_THREAD_INDEX
import json


def twittermetamodelBuilding(user_id):
    '''
    This function will be used to build the metamodel of the twitter data.
    This basically develops all the background data needed for the visualization, using Tweet data stored in DB.
    :return: -
    '''
    previouscount = 0
    userSearchObj = user_searches_ongoing[user_id]
    global TWITTER_DATA_DOWNLOADER_THREAD_INDEX
    global META_MODEL_BUILDER_THREAD_INDEX

    while(True):

        if userSearchObj.meta_model_complete and userSearchObj.tweet_fetch_complete:
            time.sleep(2)
            continue

        print userSearchObj.user_search_sentence, "From metamodel building"

        list_tweets = []
        user_tweets = {}
        hashtag_rel = {}
        list_tweets = Tweet.objects(tweet_user_search_query=userSearchObj.user_search_sentence)
        tweet_msgs_lst = []

        no_of_retweets = 0
        no_of_likes = 0
        total_posCount = 0
        total_negCount = 0

        metadata = {}

        for tweet in list_tweets:
            new_user = False
            no_of_retweets += tweet.tweet_retweets
            no_of_likes += tweet.tweet_likes

            posCount = 0
            negCount = 0

            if senana.classifier.classify(senana.feature_extractor(tweet.tweet_msg.split())) == 'positive':
                tweet.tweet_positiveOrnegative = 1
                posCount = 1
                total_posCount += 1
            else:
                tweet.tweet_positiveOrnegative = 0
                negCount = 1
                total_negCount += 1

            if user_tweets.has_key(tweet.tweet_user_handle):
                user = user_tweets[tweet.tweet_user_handle]
                user.tweet_likes += tweet.tweet_likes
                user.no_of_retweets += tweet.tweet_retweets
                user.positiveCount += posCount
                user.negativeCount += negCount
            else:
                user = Tweet_User(tweet.tweet_user_handle, tweet.tweet_user_name, tweet.tweet_user_following, tweet.tweet_user_followers, tweet.tweet_likes, tweet.tweet_retweets, posCount, negCount, 0, 0)
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
                        hashtag_obj.negativeCount += negCount
                        hashtag_obj.positiveCount += posCount
                    else:
                        hashtag_obj = Twitter_Hashtag(hashtag_string, tweet.tweet_retweets, tweet.tweet_likes, 1, posCount, negCount, 0, 0)
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

        top10Users = []
        for user in user_tweets.keys():
            user_tweets[user].user_rank = user_rank_calculator(user_tweets[user].tweet_follower, user_tweets[user].tweets.__len__(), user_tweets[user].no_of_retweets, user_tweets[user].tweet_likes)
            if top10Users.__len__() == 0:
                top10Users.append((user, user_tweets[user].user_rank))
            else:
                bfound = False
                for i in range(0, top10Users.__len__()):
                    if top10Users[i][1] < user_tweets[user].user_rank:
                        top10Users.insert(i, (user, user_tweets[user].user_rank))
                        bfound = True
                        break
                if not bfound:
                    top10Users.insert(top10Users.__len__(), (user, user_tweets[user].user_rank))

                if top10Users.__len__() > 10:
                    top10Users.__delitem__(10)

        wordlist = LanguageProcessor.Get_Common_Words_Tweets(tweet_msgs_lst, userSearchObj.configuration_parameters['max_words'])
        print userSearchObj.configuration_parameters['max_words']

        full_hashtags = full_hashtags[:full_hashtags.__len__()-1]

        posNegValues = []
        posNegValues.append(total_posCount)
        posNegValues.append(total_negCount)

        metadata.__setitem__('TotalTweets', list_tweets.__len__())
        metadata.__setitem__('TotalRetweets', no_of_retweets)
        metadata.__setitem__('TotalLikes', no_of_likes)
        metadata.__setitem__('TotalUsers', user_tweets.__len__())
        metadata.__setitem__('Hashtags', full_hashtags)
        metadata.__setitem__('Top5Hashtags', topfiveHashtags)
        metadata.__setitem__('WordList', wordlist)
        metadata.__setitem__('TopUsers', top10Users)
        metadata.__setitem__('positiveOrNegative', posNegValues)

        value = json.dumps(metadata)

        # socketIO.emit('stats', value, '/analyze')
        # emit('stats', value)
        socket_io.emit('stats', value, namespace='/analyze')
        if userSearchObj.tweet_fetch_complete is True:
            print 'Acknowledging Tweet fetch is complete'

        if previouscount == list_tweets.__len__() and userSearchObj.tweet_fetch_complete is True:
            print 'meta model build is done'
            userSearchObj.meta_model_complete = True
        else:
            previouscount = list_tweets.__len__()
        time.sleep(2)

        # socketIO.send('stats', json.dumps(metadata), '/analyze')

def user_hashtag_relationship(user_dictionary):
    new_user_dict = {}
    pass

def hashtag_hashtag_relationship(hashtag_dictionary):
    pass


def user_rank_calculator(noOfFollowers, noOfTweets, noOfRetweets, noOfLikes):
    '''
    This function will calcuate a ranking for given user.
    It depends on 4 parameters - How many people is following him/her, how many tweets user has tweeted, how many of his/her
    tweets are retweeted and how many his/her tweets are liked
    tweets, retweets, like: 0-100: 0.1, 101-1000: 0.3, 1001-10000: 0.5, 10001-100000:0.7, 100001-1000000:0.9, 1000001-infi:1
    following: 0-100: 0.1, 101-1000: 0.3, 1001-10000: 0.5, 10001-50000: 0.6, 50001-100000:0.7, 100001-1000000, 1000001-infi:1
    :param noOfFollowers: Total number of users following this user
    :param noOfTweets: Total tweets tweeted by this user
    :param noOfRetweets: Total tweets of this user retweeted
    :param noOfLikes: Total tweets of this user liked
    :return: Normalized Following Count + Normalized tweets count + Normalized retweet count + Normalized like count
    '''
    rank = 0

    normFollowers = 0
    normTweets = 0
    normRetweets = 0
    normLikes = 0

    if noOfFollowers < 100:
        normFollowers = 0.1
    elif noOfFollowers < 1000:
        normFollowers = 0.3
    elif noOfFollowers < 10000:
        normFollowers = 0.5
    elif noOfFollowers < 50000:
        normFollowers = 0.6
    elif noOfFollowers < 100000:
        normFollowers = 0.7
    elif noOfFollowers < 1000000:
        normFollowers = 0.9
    else:
        normFollowers = 1

    if noOfLikes < 100:
        normLikes = 0.1
    elif noOfLikes < 1000:
        normLikes = 0.3
    elif noOfLikes < 10000:
        normLikes = 0.5
    elif noOfLikes < 100000:
        normLikes = 0.7
    elif noOfLikes < 1000000:
        normLikes = 0.9
    else:
        normLikes = 1

    if noOfTweets < 100:
        normTweets = 0.1
    elif noOfTweets < 1000:
        normTweets = 0.3
    elif noOfTweets < 10000:
        normTweets = 0.5
    elif noOfTweets < 100000:
        normTweets = 0.7
    elif noOfTweets < 1000000:
        normTweets = 0.9
    else:
        normTweets = 1

    if noOfRetweets < 100:
        normRetweets = 0.1
    elif noOfRetweets < 1000:
        normRetweets = 0.3
    elif noOfRetweets < 10000:
        normRetweets = 0.5
    elif noOfRetweets < 100000:
        normRetweets = 0.7
    elif noOfRetweets < 1000000:
        normRetweets = 0.9
    else:
        normRetweets = 1

    rank = normFollowers + normTweets + normLikes + normRetweets

    return rank


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




