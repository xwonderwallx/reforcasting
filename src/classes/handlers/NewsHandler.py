#
# src.classes.handlers.NewsAnalyzer
#
#
#
#
#
import nltk

from src.classes.NewsAnalyzer import NewsAnalyzer
from src.classes.WebScraper import WebScraper


class NewsHandler:
    def __init__(self, currency, date):
        nltk.download('wordnet')
        nltk.download('stopwords')

        self.currency = currency
        self.date = date

    def handle(self):
        news_analyzer = NewsAnalyzer(self.get_financial_news())
        analysis = news_analyzer.analyze()
        results_str = [str(mood_state) for mood_state in analysis]
        results_joined = ', '.join(results_str)
        assert isinstance(results_joined, str)
        return results_joined

    def get_financial_news(self):
        return WebScraper().search_and_scrape(f'{self.currency} {self.date}')
