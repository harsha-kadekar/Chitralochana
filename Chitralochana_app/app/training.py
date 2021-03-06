#######################################################################################################################
# Name: training.py
# Description: This will have all the functions which will help to read or format the training data.
# references: -
# Date: 9/17/2016
#######################################################################################################################

import csv
import sys


def InputFile(filename, typeOfFile, header):
    '''
    This function given input file name and type of file will read it and convert that into a list of tweets
    with their classification of positive or negative
    :param filename: Input file name which needs to be read
    :param typeOfFile: 1 means tab separated, 0 means comma separated
    :param header: if first row represents an header in that case it is 1 else 0
    :return: list of tuples of form (sentiment, tweet text)
    '''
    list_tweets_with_classification = []
    finput = open(filename, "r")
    listLines = finput.readlines()
    finput.close()
    if header == 1:
        del(listLines[0])
    for line in listLines:
        div = []
        if typeOfFile == 1:
            div = line.split('\t')
        else:
            div = line.split(',')
        if div[0].strip() == '1':
            list_tweets_with_classification.append((1, div[1].strip()))
        else:
            list_tweets_with_classification.append((0, div[0].strip()))

    return list_tweets_with_classification


def InputFilewithCSV(filename):
    '''
    This function will parse a csv file and then gives a list of tuples with tweets and its classification as
    positive or negative
    :param filename: csv file which needs to be read
    :return: list of tweet tuples of format (sentiment, tweet text)
    '''
    list_tweets_with_classification = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Sentiment'] == '1':
                list_tweets_with_classification.append((1, row['SentimentText']))
            else:
                list_tweets_with_classification.append((0, row['SentimentText']))

    return list_tweets_with_classification

def InputFile4withCSV(filename):
    '''
    This function will parse a csv file and then gives a list of tuples with tweets and its classification as
    positive or negative
    :param filename: csv file which needs to be read
    :return: list of tweet tuples of format (sentiment, tweet text)
    '''
    list_tweets_with_classification = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Sentiment'] == '4':
                list_tweets_with_classification.append((1, row['SentimentText']))
            elif row['Sentiment'] == '0':
                list_tweets_with_classification.append((0, row['SentimentText']))

    return list_tweets_with_classification

def InputFile5withCSV(filename):
    '''
    This function will parse a csv file and then gives a list of tuples with tweets and its classification as
    positive or negative
    :param filename: csv file which needs to be read
    :return: list of tweet tuples of format (sentiment, tweet text)
    '''
    list_tweets_with_classification = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Sentiment'] == '1':
                list_tweets_with_classification.append((1, row['SentimentText']))
            elif row['Sentiment'] == '0':
                list_tweets_with_classification.append((0, row['SentimentText']))

    return list_tweets_with_classification



def FormTrainingData(training_data_path):
    file1 = r'C:\D_Drive\Coding\TestData\Twitter\SentimentAnalysis\training.txt'#'C:\D_Drive\Experiments\NLP\Twitter\sentiment_training.txt'
    file2 = r'C:\D_Drive\Coding\TestData\Twitter\SentimentAnalysis\Sentiment Analysis Dataset.csv' #'C:\D_Drive\Experiments\NLP\Twitter\Sentiment Analysis Dataset.csv'
    file3 = r'C:\D_Drive\Coding\TestData\Twitter\SentimentAnalysis\testdata.txt'#'C:\D_Drive\Experiments\NLP\Twitter\sentiment_testdata.txt'
    file4 = r'C:\D_Drive\Coding\TestData\Twitter\SentimentAnalysis\testdata.manual.2009.06.14.csv'
    # file5 = r'C:\D_Drive\Coding\TestData\Twitter\SentimentAnalysis\training.1600000.processed.noemoticon.csv'
    training_data = []
    training_data.extend(InputFile(file1, 1, 0))
    training_data.extend(InputFile(file3, 1, 0))
    training_data.extend(InputFilewithCSV(file2))
    training_data.extend(InputFile4withCSV(file4))

    outputFile = training_data_path
    trainingFile = open(outputFile, "w")

    for tp in training_data:
        line = tp[0].__str__() + '\t'+tp[1]+'\n'
        trainingFile.write(line)

    trainingFile.close()


def read_twitter_sentiment_TrainingData(training_data_path):
    listSentiments = []
    inputFile = training_data_path
    dataFile = open(inputFile, "r")
    lines = dataFile.readlines()
    dataFile.close()
    for line in lines:
        parts = line.split('\t')
        if len(parts) == 2:
            if parts[0] == '1':
                listSentiments.append((parts[1].strip(), 'positive'))
            else:
                listSentiments.append((parts[1].strip(), 'negative'))
    return listSentiments

#FormTrainingData()






