import flair
import string
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class SentimentAnalysis:
    def __init__(self):
        self._vader = SentimentIntensityAnalyzer()
        self._model = flair.models.TextClassifier.load('en-sentiment')

    def process_text(self, raw_text: str):
        # split into words
        tokens = word_tokenize(raw_text)
        # convert to lower case
        tokens = [w.lower() for w in tokens]
        # remove punctuation from each word
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]
        # remove remaining tokens that are not alphabetic
        words = [word for word in stripped if word.isalpha()]
        # filter out stop words
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]

        return ' '.join(words)

    def get_vader_polarity_scores(self, processed_text: str):
        return self._vader.polarity_scores(processed_text)

    def get_flair_score(self, processed_text: str):
        sample = flair.data.Sentence(processed_text)
        self._model.predict(sample)
        return sample.labels[0].score

    def get_textblob_sentiment(self, processed_text: str):
        return TextBlob(processed_text).sentiment

    def get_sentiments(self, text: str):
        processed_text = self.process_text(text)
        flair = self.get_flair_score(processed_text)
        polarity = self.get_textblob_sentiment(processed_text).polarity
        subjectivity = self.get_textblob_sentiment(processed_text).subjectivity
        positive = self.get_vader_polarity_scores(processed_text)['pos']
        negative = self.get_vader_polarity_scores(processed_text)['neg']
        
        return [flair, positive, negative, subjectivity, polarity]
