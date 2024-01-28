#
# src.classes.handlers.NewsAnalyzer
#
#
#
#
#

import nltk

from src.modules.news.classes.NewsAnalyzer import NewsAnalyzer
from src.modules.news.classes.WebScraper import WebScraper
from src.base.handlers.IHandler import IHandler
from collections import Counter


class NewsHandler(IHandler):
    def __init__(self, currency, date):
        nltk.download('wordnet')
        nltk.download('stopwords')

        self.currency = currency
        self.date = date

    def handle(self):
        results = []

        for news in self.get_financial_news():
            news_analyzer = NewsAnalyzer(news)
            analysis = news_analyzer.analyze()
            results.append(analysis)

        overall_sentiment = self.aggregate_sentiment(results)
        return overall_sentiment

    def get_financial_news(self):
        return WebScraper().search_and_scrape(f'{self.currency} {self.date}')

    def aggregate_sentiment(self, sentiment_list):
        # Count the number of each sentiment
        sentiment_count = Counter([sentiment for sublist in sentiment_list for sentiment in sublist])
        # Determine the sentiment with the highest count
        overall_sentiment = sentiment_count.most_common(1)[0][0]
        return overall_sentiment
