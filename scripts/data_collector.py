import re
import json
import requests
from datetime import datetime
from dateutil import parser
from bs4 import BeautifulSoup
from .twitter import TwitterClient
from .models import Tweet, Headline, Crypto


class PageNotFoundError(Exception):
    pass


class DataCollector:
    
    def __init__(self):
        self.twitter_client = TwitterClient()
        self.coinbase_products_uri = 'https://api.pro.coinbase.com/products'
        self.bitcoin_news_url = 'https://cointelegraph.com/tags/bitcoin'
        self.reddit_bitcoin_url = 'https://old.reddit.com/r/Bitcoin/'
        self.request_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }

    def _requests(self, url: str, headers: dict):
        try:
            with requests.Session() as s:
                resp = s.get(url, headers=headers)
        except Exception as error:
            raise error
        else:
            if resp.status_code == 200:
                return resp

    def _parse_bitcoin_headline(self, headline: BeautifulSoup):
        try:
            text = headline.find('span', {'class': 'post-card-inline__title'}).get_text().strip()
            published_date = parser.parse(headline.time.attrs['datetime'])
        except:
            return None
        else:
            cleaned_text = self.clean_text(text)
            if published_date.date() == datetime.today().date():
                return Headline(
                    cleaned_text, self.bitcoin_news_url,
                    published_date.strftime('%Y-%m-%d')
                )

    def _parse_reddit_post(self, post: BeautifulSoup):
        try:
            text = post.find('a', {'data-event-action': 'title'}).get_text()
            iso_formatted_date = post.time.attrs['datetime']
            published_date = parser.parse(iso_formatted_date)
        except:
            return None
        else:
            cleaned_text = self.clean_text(text)
            if published_date.date() == datetime.today().date():
                return Headline(
                    cleaned_text, self.reddit_bitcoin_url,
                    published_date.strftime('%Y-%m-%d')
                )

    def clean_text(self, text: str):
        cleaned_text = re.sub(r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', '', text)
        return cleaned_text.strip()

    def get_bitcoin_headlines(self, max_headlines: int = 10):
        bitcoin_headlines = []
        resp = self._requests(self.bitcoin_news_url, self.request_headers)
        if not resp:
            raise PageNotFoundError(f'This {self.bitcoin_news_url} cant be opened!')
        
        soup = BeautifulSoup(resp.content, 'html.parser')
        headlines = soup.find_all('li', {'class': 'posts-listing__item'})
        for headline in headlines:
            parsed_headline = self._parse_bitcoin_headline(headline)
            if parsed_headline:
                bitcoin_headlines.append(parsed_headline)

        return bitcoin_headlines[:max_headlines]

    def get_reddit_bitcoin_posts(self, max_posts: int = 10):
        reddit_posts = []
        resp = self._requests(self.reddit_bitcoin_url, self.request_headers)
        if not resp:
            raise PageNotFoundError(f'This {self.reddit_bitcoin_url} cant be opened!')
        
        soup = BeautifulSoup(resp.content, 'html.parser')
        posts = soup.find_all('div', {'class': 'top-matter'})
        for post in posts:
            parsed_reddit_post = self._parse_reddit_post(post)
            if parsed_reddit_post:
                reddit_posts.append(parsed_reddit_post)

        return reddit_posts[:max_posts]

    def get_bitcoin_tweets(self, max_tweets: int = 10):
        tweets = self.twitter_client.get_tweets(query='bitcoin', count=max_tweets)
        parsed_tweets = []
        for tweet in tweets:
            cleaned_tweet = self.clean_text(tweet.text)
            if tweet.created_at.date() == datetime.today().date():
                parsed_tweets.append(
                    Tweet(cleaned_tweet, tweet.created_at.strftime('%Y-%m-%d'))
                )

        return parsed_tweets

    def get_cryptocurrency_price(self, ticker_symbol: str = 'BTC-USD'):
        coinbase_ticker_uri = f'{self.coinbase_products_uri}/{ticker_symbol}/ticker'
        resp = self._requests(coinbase_ticker_uri, self.request_headers)
        if not resp:
            raise PageNotFoundError(f'This {self.bitcoin_news_url} cant be opened!')
        
        soup = BeautifulSoup(resp.content, 'html.parser')
        parsed_json = json.loads(soup.get_text())

        if parsed_json:
            return Crypto(
                ticker_symbol,
                parsed_json['price'],
                parsed_json['volume'],
                parser.parse(parsed_json['time']).strftime('%Y-%m-%d')
            )
