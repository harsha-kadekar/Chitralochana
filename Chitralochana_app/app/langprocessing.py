#######################################################################################################################
# Name: langprocessing.py
# Description: This file will have all the functions that necessary to the natural language processing of the given
#               sentence.
# Developer: Harsha Kadekar
# References:
# Update: 1st version - 6/7/2016
#######################################################################################################################
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


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
        tokens = word_tokenize(self.UserSentence)
        text = nltk.Text(tokens)
        tags = nltk.pos_tag(text)
        imp_words = []
        imp_words.append(self.UserSentence.lower())
        fullsentence = re.sub('[^0-9a-zA-Z]+', '', self.UserSentence).lower()
        if not imp_words.__contains__(fullsentence):
            imp_words.append(fullsentence)


        for tag in tags:
            if tag[1] == 'NNS' or tag[1] == 'NN' or tag[1] == 'NNP' or tag[1] == 'NNPS':
                if not imp_words.__contains__(tag[0].lower()):
                    imp_words.append(tag[0].lower())
        without_stopwords = [w for w in tokens if not w in stopwords.words("english")]
        for word in without_stopwords:
            if not imp_words.__contains__(word):
                imp_words.append(word.lower())




        print imp_words

        return imp_words




