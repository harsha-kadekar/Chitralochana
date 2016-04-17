'''
Name:           ConfigurationHandler
Description:    This file holds all the functions and classes responsible for the configuration of the product.
Developer:      Harsha Kadekar
References:
'''

import xml.etree.ElementTree as ET
import GeneralFunctionsandClasses as GFC


class ChitralochanaConfigurator(GFC.SingleTonClassCreator):
    '''
    Name: ChitralochanaConfiguration
    Description: This class is responsible for reading configuration file.
    '''
    def __init__(self):
        self._ConfigurationFile = 'Chitralochana.xml'
        self._LogDebugLevel = 'DEBUG'
        self._NumberOfTweetsToFetch = 200
        self._TweetTypesToFetch = 'recent'
        self._TweetFileStorage = 'Tweet_File_Storage.csv'

    # Following configuration are related to general logging
    @property
    def Log_Level(self):
        return self._LogDebugLevel

    # Following configuration are related to Tweet Analysis
    @property
    def File_Storage_Of_Tweets(self):
        return self._TweetFileStorage

    @property
    def Tweet_Fetch_Per_Call(self):
        return self._NumberOfTweetsToFetch

    @property
    def Type_Of_Tweets_To_Fetch(self):
        return self._TweetTypesToFetch

    # Following configuration are general configurations
    @property
    def Configuration_File(self):
        return self._ConfigurationFile

    def ReadTweetAnalysisConfiguration(self, ConfigRoot):
        '''
        This function reads the configuration related to tweet analysis.
        :param ConfigRoot - This is the root of the configuration xml file.
        :return: 0 for success else error code.
        '''
        return_value = 0
        twitterRoot = ConfigRoot.find('TweetAnalysis')
        generalRoot = twitterRoot.find('GeneralConfig')

        self._NumberOfTweetsToFetch = int(generalRoot.find('NumberOfTweetsToFetch').text)
        self._TweetFileStorage = generalRoot.find('FileMemory').text
        self._TweetTypesToFetch = generalRoot.find('TypeOfTweet').text

        return return_value

    def ReadLoggingConfiguration(self, ConfigRoot):
        '''
        This function reads the configuration related to logging.
        :param ConfigRoot: this is the root of the configuration xml file.
        :return: 0 for success else error
        '''
        return_value = 0
        logRoot = ConfigRoot.findall('Logging')[0]

        self._LogDebugLevel = logRoot.find('LogLevel').text

        return return_value

    def ReadConfigurationFile(self):
        '''
        This function will read the configuration file and sets all the necessary parameters needed by the
        application.
        :return:    0 for success else an error
        '''
        return_value = 0

        config = ET.parse(self._ConfigurationFile).getroot()

        #Get logging configuration
        return_value = self.ReadLoggingConfiguration(config)
        if return_value != 0:
            print 'ERROR::ConfigurationReading::Failed to read the configuraiton related to logging: ' + return_value.__str__()
            return return_value

        return_value = self.ReadTweetAnalysisConfiguration(config)
        if return_value != 0:
            print 'ERROR::ConfigurationReading::Failed to get the configuration related to tweet analysis module: ' + return_value.__str__()
            return return_value

        return return_value

    def DisplayConfigurationInformation(self):
        '''
        This function just displays all the configuration read from the file to console
        :return:
        '''

        print '===================================================================================================='
        print '===================================================================================================='
        print 'Chitralochana - Configuration info'
        print '===================================================================================================='
        print 'Configuration File ' + self._ConfigurationFile
        print '===================================================================================================='
        print 'Logging Information'
        print 'Log Level ' + self._LogDebugLevel
        print '===================================================================================================='
        print 'Tweet Analysis information '
        print 'Number of tweets fetch ' +  self._NumberOfTweetsToFetch.__str__()
        print 'Type of Tweets to fetch ' + self._TweetTypesToFetch
        print 'File storage of fetched tweets ' + self._TweetFileStorage
        print '===================================================================================================='
        print '===================================================================================================='

