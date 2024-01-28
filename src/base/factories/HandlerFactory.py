#
#
#
#
#
#
#
from src.base.enums import HandlerType
from src.modules.cdata.handlers.BinanceHandler import BinanceHandler
from src.modules.news.handlers.NewsHandler import NewsHandler


class HandlerFactory:
    @staticmethod
    def create_handler(handler_name, options=None):
        match handler_name:
            case HandlerType.BinanceHandler: return BinanceHandler(options)
            case HandlerType.NewsHandler: return NewsHandler(options['currency'], options['date'])
