#######################################################################################################################
# Name: langprocessing.py
# Description: This file will have all the functions that necessary to the natural language processing of the given
#               sentence or list of sentences.
# Developer: Harsha Kadekar
# References: http://sahandsaba.com/visualizing-philosophers-and-scientists-by-the-words-they-used-with-d3js-and-python.html
# Update: 1st version - 6/7/2016
#         2nd version - 7/25/2016
#######################################################################################################################
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re
import string
import nltk
from config import MAX_WORD_COUNTS

class LanguageProcessor(object):
    '''
    This class will be used for doing the language processing of user input and tweets
    '''

    twitter_ignore_list = ['rt', 'via'] + list(string.punctuation) + stopwords.words('english')
    twitter_emoticons_str = r"""
        (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
        )"""
    twitter_regex_str = [
        twitter_emoticons_str,
        r'<[^>]+>', # HTML tags
        r'(?:@[\w_]+)', # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",   # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',   # URLs
        r'(?:(?:\d+,?)+(?:\.?\d+)?)',   # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])",    # words with - and '
        r'(?:[\w_]+)',  # other words
        r'(?:\S)'   # anything else
        ]

    twitter_tokens_re = re.compile(r'(' + '|'.join(twitter_regex_str) + ')', re.VERBOSE | re.IGNORECASE)
    twitter_emoticon_re = re.compile(r'^' + twitter_emoticons_str + '$', re.VERBOSE | re.IGNORECASE)

    @staticmethod
    def GetImportantWordsFromSentence(sentence):
        '''
        This function given a sentence, tries to find the important words or phrases from that sentence.
        If its a single word then it will just past it back.

        TODO: As of now this is not proper. It needs to be improved

        :param sentence: Usually anysentence would be fine. But in our context it is User query sentence.
        :return: list of important words or sentences pertaining to given sentence
        '''
        tokens = word_tokenize(sentence)
        text = nltk.Text(tokens)
        tags = nltk.pos_tag(text)
        imp_words = []
        imp_words.append(sentence.lower())
        fullsentence = re.sub('[^0-9a-zA-Z]+', '', sentence).lower()
        if not imp_words.__contains__(fullsentence.strip()):
            imp_words.append(fullsentence)

        print 'tag processing'
        for tag in tags:
            if tag[1] == 'NNS' or tag[1] == 'NN' or tag[1] == 'NNP' or tag[1] == 'NNPS':
                if not imp_words.__contains__(tag[0].lower().strip()):
                    print tag[0].lower()
                    imp_words.append(tag[0].lower())
        without_stopwords = [w for w in tokens if not w in stopwords.words("english")]
        print 'word processing'
        for word in without_stopwords:
            if not imp_words.__contains__(word.strip().lower()):
                print word.lower()
                imp_words.append(word.lower())

        return imp_words

    @staticmethod
    def Get_Common_Words_Tweets(Msg_List):
        '''
        This function will get first divide each tweets into words. Get the count of each words. Then return top 200 words with their count
        :param Msg_List: This is the list of tweet messages which will be analyzed
        :return: list of most common words with their count.
        '''
        count_all = Counter()
        emoji_re = re.compile(u'('
                              u'\ud83c[\udf00-\udfff]|'
                              u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                              u'\u2026|'
                              u'\ufe0f|'
                              u'[\u2600-\u26FF\u2700-\u27BF])+',
                              re.UNICODE)

        for tweet in Msg_List:
            tweet = emoji_re.sub('', tweet)
            list_tokens = [tokens for tokens in LanguageProcessor.twitter_tokens_re.findall(tweet) if tokens.lower() not in LanguageProcessor.twitter_ignore_list and not tokens.startswith('https:') and tokens.__len__() > 1]
            count_all.update(list_tokens)
        return count_all.most_common(MAX_WORD_COUNTS)






