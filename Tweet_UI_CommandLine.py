'''
Name:           Tweet_UI_CommandLine
Description:    This file will hold all the functions and classes related to command line interface of the
                TweetAnalysis.
Developer:      Harsha Kadekar
'''

import sys as System
import ConfigurationHandler as configLib

CommandLine_User_Input_tweetanalysis = ''


# This is the starting point of the command line interface of the Chitralochanas twitter analysis.
if __name__ == '__main__':
    print 'Tweet Analysis:-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-'
    print '-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+'
    if System.argv > 1:
        print 'Given user input: ' + System.argv[1]
        CommandLine_User_Input_tweetanalysis = System.argv[1]
        config = configLib.ChitralochanaConfigurator()
        return_value = config.ReadConfigurationFile()
        if return_value != 0:
            print 'ERROR:: Not able to read configuration so exiting '
        else:
            config.DisplayConfigurationInformation()

    else:
        print 'ERROR:: Tweet Analysis:: No command line user input provided.'
        print 'USAGE:: Tweet_UI_CommandLine <<User input in quotes>>'
    print 'Closing Tweet Analysis:+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+'
    print '-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+'

