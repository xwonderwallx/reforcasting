import re
import nltk
from bs4 import BeautifulSoup
from nltk import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from src.enums.MoodState import MoodState


class NewsAnalyzer:
    def __init__(self, news):
        self.news = news

    def analyze(self):
        analyzer = SentimentIntensityAnalyzer()
        results = []

        for article in self.news:
            preprocessed_text = self.preprocess_text(article)
            sentiment_vader = analyzer.polarity_scores(preprocessed_text)
            sentiment_textblob = TextBlob(preprocessed_text).sentiment.polarity
            mood_state = self.sentiment_analysis(sentiment_vader, sentiment_textblob)
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
