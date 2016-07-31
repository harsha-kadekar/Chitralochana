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
import tweepy
from app import socketIO, userSentence, metamodelThread
from tweepy import OAuthHandler
from config import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, MAX_FETCH_TWEETS, MONGODB_SETTINGS, MAX_WORD_COUNTS
from relations import Tweet_User, Twitter_Hashtag
from mongoengine import connect
from models import Tweet
from nltk.corpus import stopwords
from collections import Counter
import re
import time
import string
from flask_socketio import emit
import thread
import json

completeTweetFetch = False
completedMetaModel = False

class WordCloudGenerator(object):
    def __init__(self, list_of_messages):
        self.Msg_List = list_of_messages
        self.ignore_list = ['rt', 'via'] + list(string.punctuation) + stopwords.words('english')
        # ------------Start------------------------
        # following code taken from https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/
        self.emoticons_str = r"""
        (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
        )"""
        self.regex_str = [
            self.emoticons_str,
            r'<[^>]+>', # HTML tags
            r'(?:@[\w_]+)', # @-mentions
            r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
            r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
            r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
            r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
            r'(?:[\w_]+)', # other words
            r'(?:\S)' # anything else
            ]

        self.tokens_re = re.compile(r'('+'|'.join(self.regex_str)+')', re.VERBOSE | re.IGNORECASE)
        self.emoticon_re = re.compile(r'^'+self.emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

        #--------- End--------------------

    def process(self):
        count_all = Counter()
        emoji_re = re.compile(u'('
                              u'\ud83c[\udf00-\udfff]|'
                              u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                              u'\u2026|'
                              u'\ufe0f|'
                              u'[\u2600-\u26FF\u2700-\u27BF])+',
                              re.UNICODE)

        for tweet in self.Msg_List:
            tweet = emoji_re.sub('',tweet)
            list_tokens = [tokens for tokens in self.tokens_re.findall(tweet) if tokens.lower() not in self.ignore_list and not tokens.startswith('https:') and tokens.__len__() > 1]
            count_all.update(list_tokens)
        return count_all.most_common(MAX_WORD_COUNTS)

def GetPastTweets(searchStrings):
    auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)


    deleteEntries = connect(MONGODB_SETTINGS['DB'])
    deleteEntries.drop_database(MONGODB_SETTINGS['DB'])

    listTweetIDs = []

    global completeTweetFetch
    global completedMetaModel
    global userSentence
    global metamodelThread

    user_query = userSentence

    completeTweetFetch = False
    completedMetaModel = False

    for searchString in searchStrings:
        searchTweets = [status for status in tweepy.Cursor(api.search, q=searchString).items(MAX_FETCH_TWEETS)]

        # searched_tweets = []
        # last_id = -1
        # while len(searched_tweets) < max_tweets:
        # count = max_tweets - len(searched_tweets)
        # try:
            # new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
            # if not new_tweets:
                #break
            # searched_tweets.extend(new_tweets)
            # last_id = new_tweets[-1].id
        # except tweepy.TweepError as e:
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            #break

        # somefile = io.open('dump.txt', 'a', encoding='utf-8')
        # dump = searchTweets.__str__().encode('utf-8')
        # somefile.write(unicode(dump))
        # somefile.close()
        for tweet in searchTweets:
            tweet_id = tweet.id
            if listTweetIDs.__contains__(tweet_id):
                continue
            if len(Tweet.objects(tweet_id=tweet_id)) > 1:
                continue
            tweet_message = tweet.text.encode("utf-8")
            tweet_userhandle = tweet.user.screen_name
            tweet_retweet_count = tweet.retweet_count
            tweet_createtime = tweet.created_at
            tweet_location = None
            tweet_geo = None
            tweet_favoritecount = tweet.favorite_count
            tweet_username = tweet.user.name
            tweet_user_no_of_following = tweet.user.friends_count
            tweet_user_no_of_followers = tweet.user.followers_count
            tweet_positiveOrnegative = 0
            tweet_polarOrneutral = 0
            tweet_isRetweet = 0

            oneTweet = Tweet(tweet_id=tweet_id, tweet_msg=tweet_message, tweet_likes=tweet_favoritecount, tweet_retweets=tweet_retweet_count, tweet_search_category=searchString, tweet_user_search_query=user_query, tweet_positiveOrnegative=tweet_positiveOrnegative, tweet_polarOrneutral=tweet_polarOrneutral, tweet_user_handle=tweet_userhandle, tweet_user_name=tweet_username, tweet_user_followers=tweet_user_no_of_followers, tweet_user_following=tweet_user_no_of_following, tweet_isretweet=tweet_isRetweet, tweet_time=tweet_createtime, tweet_location=tweet_location, tweet_geo=tweet_geo)
            oneTweet.save()
            listTweetIDs.append(tweet_id)
            if metamodelThread is None:
                metamodelThread = thread.start_new_thread(metamodelBuilding, ())

    print 'completed tweet fetch'
    completeTweetFetch = True


def metamodelBuilding():

    global completeTweetFetch
    global userSentence
    global completedMetaModel

    previouscount = 0

    while(True):

        if completedMetaModel and completeTweetFetch:
            time.sleep(2)
            continue

        list_tweets = []
        user_tweets = {}
        hashtag_rel = {}
        list_tweets = Tweet.objects(tweet_user_search_query=userSentence)
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

        wordlist = wordCloudGeneration(tweet_msgs_lst)
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
        if previouscount == list_tweets.__len__() and completeTweetFetch == True:
            print 'meta model build is done'
            completedMetaModel = True
        else:
            previouscount = list_tweets.__len__()
        time.sleep(2)


        # socketIO.send('stats', json.dumps(metadata), '/analyze')

def wordCloudGeneration(list_tweet_msgs):
    wordCloud = WordCloudGenerator(list_tweet_msgs)
    return wordCloud.process()



