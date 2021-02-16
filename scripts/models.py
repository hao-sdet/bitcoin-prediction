from dataclasses import dataclass


@dataclass
class Headline:
    headline: str
    source: str
    published_date: str


@dataclass
class Tweet:
    tweet: str
    tweeted_date: str


@dataclass
class Crypto:
    ticker: str
    price: float
    volume: float
    updated_at: str
