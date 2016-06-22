# Chitralochana
This is a tool to analyze and visualize the social network buzz.

It has 3 main work - fetch meaningful data, analyze that data and finally visualize the information drawn out of that data.

Fetch meaningful data - Social network as of now mainly consists of 2 main websites or platform: Facebook and Twitter. So fetching meaningful data means better ways for scrapping the tweets from twitter as well as useful information from facebook. For twitter I will be using Tweepy and for facebook I will be using facebook-sdk

Analyze data - Once I have retrieved that data, I will try to build model on that data. In case of twitter various relationships like tweet, its user, search category, hashtag, etc. For facebook I am yet to figure it out. Apart from this model building various analysis will be done like - sentiment analysis, trying to get the word cloud of all the data, among the searched strings which hashtag is more popular, try to get the summary of what is going on based on all the data, then geo location analysis and similarly time lapse of the data production.

Visualize information - After doing various analysis, that information or result will be showed in the form of various graphs and other visualization forms so that user can get it in a better format.

Development - This is will be a website. Website development will be done using python flask. For twitter interaction, I will be using Tweepy. Similarly for facebook interaction I will be using facebook-sdk. Finally for graphs and visualization, I will be using d3.js . I am yet to think of storage of data. In that case most probably I will be using mongodb. For frontend, I might use AngularJS. For styling purpose I will be using boostrap.
