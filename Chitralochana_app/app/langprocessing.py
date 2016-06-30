#######################################################################################################################
# Name: langprocessing.py
# Description: This file will have all the functions that necessary to the natural language processing of the given
#               sentence.
# Developer: Harsha Kadekar
# References:
# Update: 1st version - 6/7/2016
#######################################################################################################################
from app import tweetThread, userSentence
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import thread
from twitter import GetPastTweets


class LanguageProcessor:
    def __int__(self):
        self.user_sentence = ''

    @property
    def UserSentence(self):
        return self.user_sentence

    @UserSentence.setter
    def UserSentence(self, value):
        self.user_sentence = value

    def GetImportantWords(self):
        tokens = word_tokenize(self.user_sentence)
        text = nltk.Text(tokens)
        tags = nltk.pos_tag(text)
        imp_words = []
        imp_words.append(self.user_sentence.lower())
        fullsentence = re.sub('[^0-9a-zA-Z]+', '', self.user_sentence).lower()
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


def userProcessingandTwitterdownloadInitiator(user_sentence):
    langProc = LanguageProcessor()
    global tweetThread
    print user_sentence
    langProc.user_sentence = user_sentence
    # print langProc.user_sentence
    imp_words = langProc.GetImportantWords()

    tweetThread = thread.start_new_thread(GetPastTweets, (imp_words, ))



