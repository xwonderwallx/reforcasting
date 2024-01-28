#
#
#
#
#
#
#
from src.modules.news.handlers.NewsHandler import NewsHandler


class NewsSeeker:
    def __init__(self, currency='', date=''):
        self.currency = currency
        self.date = date

    def seek(self):
        news_handler = NewsHandler(currency=self.currency, date=self.date)
        return news_handler.handle()
