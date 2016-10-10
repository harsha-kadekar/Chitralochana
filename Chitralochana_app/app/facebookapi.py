#######################################################################################################################
# Name: facebookcalls.py
# Description: This file has functions to fetch posts from facebook
# Developer: Harsha
# Reference:
# Update: 1st Version 6/22/2015
#######################################################################################################################
from config import FACEBOOK_APP_ID, FACEBOOK_SECRET_KEY
#from facebook import GraphAPI
import urllib2
import json

def GetPosts(searchStrings):
    token = FACEBOOK_APP_ID + '|' + FACEBOOK_SECRET_KEY
    str = ''
    new_string = searchStrings.replace(' ','+')
    graph_url = '/search?q='+searchStrings+'&type=page'
    print graph_url
    #graph = GraphAPI(access_token=token)
    #str = graph.request(graph_url)

    print ''


