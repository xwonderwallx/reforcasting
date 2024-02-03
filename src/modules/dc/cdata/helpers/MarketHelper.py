#
#
#
#
import csv

from src.modules.dc.cdata.handlers.BinanceHandler import BinanceHandler


class MarketHelper:
    @staticmethod
    def execute_binance_data_collection(params):
        return BinanceHandler(params=params).handle()
