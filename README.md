Welcome to the SocialBuzz(Chitralochana) wiki!

This a website which helps for analyzing the social network chatter. Main idea of this website is, given a topic it should mine the social networks mainly twitter and facebook and collect the information regarding that topic. Once sufficient data has been obtained it should start the analysis of it. Finally after some analysis, it should show that in some kind of visualization so that users can grasp that analysis

Demo -

[![ScreenShot](https://drive.google.com/open?id=0BxQoWoSofKvaOG1pMUI4MHRYTWM)](https://drive.google.com/open?id=0BxQoWoSofKvaVEZydkFhYzlRTms)

Technology used - python, python - flask, d3.js, bootstrap css package, nltk, facebook-sdk, tweepy

As of now following analysis and visualization is done
1. Top 10 hashtags related to query string [visualization using a bar chart]
2. Top 10 user handles related to query string [visualization yet to be done]
3. Word Net - a cloud of words represented based on their frequency usage.
4. Sentiment Analysis - Total percentage of positive verses negative opinium about the given user query. [Visualization using pie chart]

Some of the analysis to be done
1. Show how user - tweets relationship - This gives you an idea of how the topic is been discussed. Whether many people are discussing about the topic or few users are discussing about the topic. Something like m-n connections. Is m less in number but n greater in number? Is m greater in number and n lesser in number? Is both m and n less in number? Is both m and n greater in number?

2. Show hashtag relationship - This gives an idea of how this topic is related to other topics.

3. Time lapse of the tweets -  How the interest regarding the topic is varying in time.

4. Location analysis - To which geographic location this topic is generating interest

5. Polarity Analysis - Neutral/Polar

10. A summary of the discussion.

11. Clusterring of similar type of tweets

For sentiment analysis we have used NaiveBayesClassifier. So for this project we are using Natural language processing and Machine learning algorithms.

