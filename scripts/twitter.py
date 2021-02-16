import re
import tweepy
from tweepy import OAuthHandler


class TwitterAuthenticationError(Exception):
    pass


class RetrievingTweetDataFailedError(Exception):
    pass


consumer_key = 'MOe623rxcqck6x8y5XhzK8MJT'
consumer_secret = 'mcBq9Km1f3OYERRD6vKmOfWSgCjsqzXAreIsn8klxAtPIo40E7'
access_token = '913787859630460928-RXF8NVN3gGbxD64NCZ7wBma5M2WPwlv'
access_secret = 'P4UU9I2DimdnUown2EM6p4WZ0ftdPNsysDNW6xGh0Ts4f'


class TwitterClient:
    
    def __init__(self):
        try: 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            self.auth.set_access_token(access_token, access_secret) 
            self.api = tweepy.API(self.auth) 
        except: 
            raise TwitterAuthenticationError('Could not connect to twitter API.')
  
    def get_tweets(self, query: str, count: int = 10): 
        tweets = [] 
        try: 
            fetched_tweets = self.api.search(q=query, count=count) 
            for tweet in fetched_tweets: 
                if tweet.retweet_count > 0: 
                    if tweet not in tweets: 
                        tweets.append(tweet) 
                else: 
                    tweets.append(tweet)

        except tweepy.TweepError as e: 
            raise RetrievingTweetDataFailedError(
                'An error occured while retrieving data from twitter.'
            ) from e 
        else:
            return tweets
