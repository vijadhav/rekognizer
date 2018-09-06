#!/usr/bin/python3
import re
import tweepy
from tweepy.auth import OAuthHandler
from textblob import TextBlob

## 
##  NLP Client using Tweepy
##

def percentage (part, whole) :
	return round(100 * float(part) / float(whole), 2)
 
class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = '8UgS5l2FkAVHWAAVp9AgvosuR'
        consumer_secret = 'gH7vykfVJClxhyIQsFX3QA7GB1uLhnwI0aKKTra9qaXU2A2iXe'
        access_token = '17701667-uz9qnl8ruo3RM2lQXqBrisLoJ2WtnRmbvX8TFXYHa'
        access_token_secret = 'UZUOgDBhrQxIabhxoTCd9x1A6Mbb7RWmIe09zMEtdR9wt'
        
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        #return str(tweet.encode('utf-8', errors='ignore'))
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        analysis = TextBlob(self.clean_tweet(tweet))

        '''
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
        '''
        return analysis.sentiment.polarity
 
    def get_tweets(self, query, limit=100):
        '''
        Main function to fetch tweets and parse them.
        '''
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            # fetched_tweets = self.api.search(q=query, count=limit, tweet_mode='extended', lang='en')

            total_tweets = 0
            for tweet in tweepy.Cursor(self.api.search, q=query, count=limit, tweet_mode="extended", lang="en").items(limit):
                total_tweets += 1
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.full_text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.full_text)
 
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            print ('Total {} tweets fetched'.format(total_tweets))
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            print("Error : " + str(e))

         
def tweetlyze (topic: str, no_of_tweets: int) -> 'list' :
    api = TwitterClient()
    
    # topic = input ('Enter Topic/HashTag: ')
    # no_of_tweets = int(input ('How many tweets: '))

    tweets = api.get_tweets(topic, no_of_tweets)
 	
    print ('post clean-up, got {} tweets to analyze'.format (len(tweets)))
    '''
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    print("Neutral tweets percentage: {} % \
        ".format(100 * (len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
    '''

    positive_tweets = 0
    negative_tweets = 0
    neutral_tweets = 0
    polarity = 0

    for tweet in tweets :
        msg = ''.join(c for c in tweet['text'] if c <= '\uFFFF')
        print ("Tweet: ", '"', msg, '"')
        print ('Sentiment : ', round(tweet['sentiment'], 4), '(',
            'Positive' if tweet['sentiment'] > 0.0 else 'Neutral' if tweet['sentiment'] == 0 else 'Negative', ')')
        print ()
        #analysis = TextBlob (tweet['text'])
        polarity += tweet['sentiment']

        if tweet['sentiment'] == 0:
            neutral_tweets += 1
        elif tweet['sentiment'] < 0.0 :
            negative_tweets += 1
        elif tweet['sentiment'] > 0.0 :
            positive_tweets += 1

    print ("SUMMARY: ")

    print ("Overall  ...", end="")
    if polarity == 0 :
        print ("Neutral")
    elif polarity < 0 :
        print ("Negative")
    elif polarity > 0 :
        print ("Positive")

    print ("Positive : ", positive_tweets, " (", percentage (positive_tweets, len(tweets)) if len(tweets) > 0 else 0, "% )")
    print ("Negative : ", negative_tweets, " (", percentage (negative_tweets, len(tweets)) if len(tweets) > 0 else 0, "% )")
    print ("Neutral  : ", neutral_tweets, " (", percentage (neutral_tweets, len(tweets)) if len(tweets) > 0 else 0, "% )")
    return tweets


if __name__ == "__main__":
    # calling main function
    main()
