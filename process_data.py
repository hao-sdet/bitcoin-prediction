import numpy as np
from statistics import mean
from pathlib import Path
from sentiment_analysis import SentimentAnalysis
from database import MySqlClient, MySqlConfiguration
from database.exceptions import (
    DatabaseConnectionError, DatabaseInsertionError,
    DatabaseQueryError
)

HOST = '127.0.0.1'
USERNAME = 'admin'
PASSWORD = 'password1'
DATABASE = 'bitcoin'

CSV_OUT_FILE = Path.cwd() / 'data' / 'merged_data.csv'

start_date = '2021-01-06'
end_date = '2021-01-07'
ticker_symbol = 'BTC-USD'

get_bitcoin_price_data_query = (
    'SELECT ticker, price, updated_at FROM cryptos '
    f'WHERE ticker="{ticker_symbol}" AND updated_at BETWEEN "{start_date}" AND "{end_date}"'
)
get_tweet_data_query = (
    'SELECT tweet, tweeted_date FROM tweets ' 
    f'WHERE tweeted_date BETWEEN "{start_date}" AND "{end_date}"'
)
get_headline_data_query = (
    'SELECT headline, published_date FROM headlines '
    f'WHERE published_date BETWEEN "{start_date}" AND "{end_date}"'
)

mysql_config = MySqlConfiguration(
    address=HOST, user=USERNAME,
    password=PASSWORD, database=DATABASE
)
mysql_client = MySqlClient(mysql_config)
try:
    mysql_client.connect()
except DatabaseConnectionError as error:
    print(error)
else:
    try:
        bitcoin_price_df = mysql_client.get_dataframe(query=get_bitcoin_price_data_query, index_column='updated_at')
        tweet_df = mysql_client.get_dataframe(query=get_tweet_data_query, index_column='tweeted_date')
        headline_df = mysql_client.get_dataframe(query=get_headline_data_query, index_column='published_date')
    except DatabaseQueryError as error:
        print(error)

# Clsoe the connection
mysql_client.close()

# Process data
merged_data = bitcoin_price_df
sentiment_columns = ['price', 'flair', 'positive', 'negative', 'subjectivity', 'polarity']
merged_data = merged_data.reindex(columns=sentiment_columns)   
sa = SentimentAnalysis()
for index, row in merged_data.iterrows():
    tweets = tweet_df.loc[tweet_df.index == index][:30]
    headlines = headline_df.loc[headline_df.index == index][:20]
    # Combine tweets with headlines
    merged_text = tweets['tweet'].tolist()
    merged_text.extend(headlines['headline'].tolist())
    sentiments = sa.get_sentiments(text=' '.join(merged_text))
    # Append new columns
    i = merged_data.index.get_loc(index)
    merged_data['price'][i] = bitcoin_price_df['price'][i]
    merged_data['flair'][i] = sentiments[0]
    merged_data['positive'][i] = sentiments[1]
    merged_data['negative'][i] = sentiments[2]
    merged_data['subjectivity'][i] = sentiments[3]
    merged_data['polarity'][i] = sentiments[4]

# Export dataframe to csv
csv_file_name = CSV_OUT_FILE
merged_data.to_csv(csv_file_name, encoding='utf-8')
