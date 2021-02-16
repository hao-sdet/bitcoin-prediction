from dataclasses import astuple
from scripts import DataCollector
from database import MySqlClient, MySqlConfiguration
from database.exceptions import (
    DatabaseConnectionError, DatabaseInsertionError
)

HOST = '127.0.0.1'
USERNAME = 'admin'
PASSWORD = 'password1'
DATABASE = 'bitcoin'

# Mysql database configuration
mysql_config = MySqlConfiguration(
    address=HOST, user=USERNAME,
    password=PASSWORD, database=DATABASE
)
mysql_client = MySqlClient(mysql_config)

# Sql queries
add_bitcoin_headline = ('INSERT INTO headlines '
            '(headline, source, published_date) '
            'VALUES (%s, %s, %s)')
add_bitcoin_tweet = ('INSERT INTO tweets '
            '(tweet, tweeted_date) '
            'VALUES (%s, %s)')
add_crypto_price = ('INSERT INTO cryptos '
            '(ticker, price, volume, updated_at) '
            'VALUES (%s, %s, %s, %s)')

# Collect bitcoin data (tweets, headline news, reddit posts)
data_collector = DataCollector()
headlines = data_collector.get_bitcoin_headlines(max_headlines=10)
headlines.extend(data_collector.get_reddit_bitcoin_posts(max_posts=25))
tweets = data_collector.get_bitcoin_tweets(max_tweets=50)
bitcoin = data_collector.get_cryptocurrency_price()
ether = data_collector.get_cryptocurrency_price('ETH-USD')
lite = data_collector.get_cryptocurrency_price('LTC-USD')

#Create connection with mysql database
try:
    mysql_client.connect()
except DatabaseConnectionError as error:
    print(error)
else:
    try:
        mysql_client.insert_multiple(
            query=add_bitcoin_headline, data=[astuple(headline) for headline in headlines]
        )
        mysql_client.insert_multiple(
            query=add_bitcoin_tweet, data=[astuple(tweet) for tweet in tweets]
        )
        mysql_client.insert_multiple(
            query=add_crypto_price, data=[astuple(crypto) for crypto in [bitcoin, ether, lite]]
        )
    except DatabaseInsertionError as error:
        print(error)

# Close the connection
mysql_client.close()
