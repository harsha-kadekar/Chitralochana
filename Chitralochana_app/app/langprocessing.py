#######################################################################################################################
# Name: langprocessing.py
# Description: This file will have all the functions that necessary to the natural language processing of the given
#               sentence or list of sentences.
# Developer: Harsha Kadekar
# References: http://sahandsaba.com/visualizing-philosophers-and-scientists-by-the-words-they-used-with-d3js-and-python.html
#             http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
# Update: 1st version - 6/7/2016
#         2nd version - 7/25/2016
#######################################################################################################################
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re
import string
import nltk
import random
import datetime
from config import MAX_WORD_COUNTS
from training import read_twitter_sentiment_TrainingData

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

    @staticmethod
    def get_minimum_edit_distance(msg1, msg2):
        '''
        This function will calculate the minimum edit distance between two strings.
        Basically how many minimum operations you do on msg1 to get msg2. You can do
        3 types of operations = either addition, deletion or update.
        It is calculated using dynamic programming
        :param msg1: it is the string which needs to be converted to msg2
        :param msg2: it is the reference string to which msg1 needs to be converted
        :return: miminum edit distance to convert msg1 to msg2
        '''
        m = msg1.__len__()
        n = msg2.__len__()

        distMatrix = []

        for i in range(0, m+1):
            distMatrix.append([])
            for j in range(0, n+1):
                distMatrix[i].append([])

        distMatrix[0][0] = 0

        for i in range(1, m+1):
            distMatrix[i][0] = i

        for j in range(1, n+1):
            distMatrix[0][j] = j

        for i in range(1, m+1):
            for j in range(1, n+1):
                val = 0
                if msg1[i-1] == msg2[j-1]:
                    val = 0
                else:
                    val = 2
                distMatrix[i][j] = min(distMatrix[i-1][j]+1, distMatrix[i][j-1]+1, distMatrix[i-1][j-1] + val)


        return distMatrix[m][n]



class SentimentAnalyzer(object):
    '''
    This class is used for the sentiment analysis. It will classify the given tweet into a positive or negative
    Currently it is using NaiveBayes Classifier and total of 1000 tweets. Later on it will be improved.
    Feature selection is also very basic. It is just removing words whose length is less than 2
    '''
    def __init__(self):
        '''
        This is our constructor.
        Used to initialize different data
        '''
        self.word_features = []
        self.training_data = []
        self.test_data = []
        self.classifier = None

    def Get_Frequency_Distribution(self, list_words):
        '''
        This function will give the frequency distribution of the list of words passed.
        :param list_words: list of words whose frequency distribution needs to be calculated
        :return: Frequency distribution of the list of words
        '''
        wordlist = nltk.FreqDist(list_words)
        return wordlist

    def feature_extractor(self, document):
        '''
        This function will give the features of the given tweets.
        Given the list of words of a tweet, it will return a dictionary having
        key as all the words of the training set and then value as true if tweet has
        this word or not.
        :param document: list of words of a tweet
        :return: a dictionary key as word and value true/false if the word is in tweet
        '''
        document_words = set(document)
        features = {}
        for word in self.word_features:
            features['contains '+word] = (word in document_words)
        return features

    def sentiment_analysis_training(self):
        '''
        This is the function which will develop the model which will help us to classify a tweet
        whether it is positive or negative. As of now it is using NaiveBayes Classifier.
        Currently all the words of the tweet are put into word features. It needs to be changed
        in future.
        :return: -
        '''
        listtrainingtweets = read_twitter_sentiment_TrainingData()
        list_words = []
        read_data = []
        dev_test = []
        dev_training = []
        for row in listtrainingtweets:
            words_filtered = [e.lower() for e in row[0].split() if len(e) > 2]
            read_data.append((words_filtered, row[1]))

        random.shuffle(read_data)

        self.training_data = read_data[len(read_data)/2:]
        self.test_data = read_data[:len(read_data)/2]

        # dev_training = self.training_data[len(self.training_data)/2:]
        # dev_test = self.training_data[:len(self.training_data)/2]

        dev_training = self.training_data[0:10000]
        dev_test = self.training_data[10001:20001]

        for (words, senti) in dev_training:
            list_words.extend(words)

        feat = self.Get_Frequency_Distribution(list_words)
        max_1000 = feat.most_common(10000)

        self.word_features = [word for (word, count) in max_1000]

        # featuresSets = [(self.feature_extractor(wordlist), sentiment) for (wordlist, sentiment) in read_data]

        # self.training_data = read_data[read_data.__len__()/2:]
        # self.test_data = read_data[:read_data.__len__()/2]

        # classifer = nltk.NaiveBayesClassifier.train(self.training_data)
        self.training_data = nltk.classify.apply_features(self.feature_extractor, dev_training)
        dev_test_data = nltk.classify.apply_features(self.feature_extractor, dev_test)
        # for (words, label) in dev_training:


        # self.test_data = nltk.classify.apply_features(self.feature_extractor, dev_test)

        self.classifier = nltk.NaiveBayesClassifier.train(self.training_data)
        print nltk.classify.accuracy(self.classifier, dev_test_data)
        print self.classifier.most_informative_features(32)

#senana = SentimentAnalyzer()
#print datetime.datetime.now()
#senana.sentiment_analysis_training()
#print datetime.datetime.now()

















