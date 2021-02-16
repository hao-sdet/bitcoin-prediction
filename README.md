# Getting Started

## Requirements
+ Python 3.8
+ Pipenv
+ Docker

## Setup
### Build Mysql Database Container
```
$ cd database/
$ docker build -t bitcoin-mysql-image:local 
$ docker run --detach --name bitcoin-mysql-container -p 3306:3306 bitcoin-mysql-image:local
$ docker exec -it bitcoin-mysql-container bash
```
### Install Dependencies using Pipenv
```
$ pipenv install --ignore-pipfile
```
### Update Mysql Database with Data
The miner script collects data from four different sources (coinbase, reddit, twitter, and cointelegraph), cleans,
and submits these into Mysql database
```
$ python miner.py 
```

### Processing Data
The process data script gets data(headlines, tweets, coins prices) from Mysql database and applies Sentiment Analysis then store the results
into a csv file called data/merged_data.csv
```
$ python process_data.py 
```