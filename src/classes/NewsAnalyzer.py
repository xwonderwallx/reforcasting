import re
import nltk
from bs4 import BeautifulSoup
from nltk import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from src.enums.MoodState import MoodState
from transformers import pipeline


class NewsAnalyzer:
    def __init__(self, news):
        self.news = news
        self.sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    def analyze(self):
        # analyzer = SentimentIntensityAnalyzer()
        results = []

        # for article in self.news:
        #     # preprocessed_text = self.preprocess_text(article)
        #     print(article)
        #     sentiment_vader = analyzer.polarity_scores(article)
        #     sentiment_textblob = TextBlob(article).sentiment.polarity
        #     mood_state = self.sentiment_analysis(sentiment_vader, sentiment_textblob)
        #     results.append(mood_state)
        #
        # return results
        for article in self.news:
            sentiment_result = self.sentiment_pipeline(article)
            sentiment_label = sentiment_result[0]['label']
            mood_state = self.convert_label_to_mood_state(sentiment_label)
            results.append(mood_state)
        return results

    def sentiment_analysis(self, sentiment_vader, sentiment_textblob):
        if sentiment_vader['compound'] >= 0.05 and sentiment_textblob > 0:
            return MoodState.POSITIVE
        elif sentiment_vader['compound'] <= -0.05 and sentiment_textblob < 0:
            return MoodState.NEGATIVE
        else:
            return MoodState.NEUTRAL

    def preprocess_text(self, text):
        soup = BeautifulSoup(text, "html.parser")
        text = soup.get_text(separator=" ")

        text = text.lower()

        text = re.sub(r'\W', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        stemmer = PorterStemmer()
        lemmatizer = WordNetLemmatizer()
        nltk.download('wordnet')
        nltk.download('stopwords')
        stop_words = set(stopwords.words('english'))

        tokens = text.split()
        tokens = [stemmer.stem(lemmatizer.lemmatize(token)) for token in tokens if token not in stop_words]

        return ' '.join(tokens)

    def concat_article(self, article_list):
        concatenated_news = []
        for sublist in article_list:
            concatenated_string = ' '.join(sublist)
            concatenated_news.append(concatenated_string)
        return concatenated_news

    @staticmethod
    def convert_label_to_mood_state(label):
        if label == 'POSITIVE':
            return MoodState.POSITIVE
        elif label == 'NEGATIVE':
            return MoodState.NEGATIVE
        else:
            return MoodState.NEUTRAL
