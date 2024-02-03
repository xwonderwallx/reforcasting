# BinanceHandler.py
#
#
# Binance date handler
# Getting and saving Binance data from Binance API to local csv file as a local data storage
# use handle() to process the data from Binance API
#
#

import ccxt
from src.base.handlers.IHandler import IHandler
from src.base.helpers.CsvHelper import CsvHelper


class BinanceHandler(IHandler):

    @property
    def exchange(self):
        return self.__exchange

    def __init__(self, params=None):
        """
        expects an array here:
        Args:
            params = [
                'data' => None,
                'symbol' => 'BTCUSDT',
                'timeframe' => '1d',
                'limit' => 1000,
                'days' => 365
            ]
        """
        self.__params = params
        self.__exchange = ccxt.binance()

    # from abstract DataHandler.php
    def handle(self):
        return self.__get_and_save_binance_data()

    def __get_and_save_binance_data(self):
        # # TODO: markets for rate
        # # TODO: set format of date : array({day: d, rate: r}, {}, {}, {}, {})
        symbol = self.__get_currency_symbol()
        print(symbol)
        timeframe = self.__get_timeframe_alias()
        # url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        # path_to_file = f'../binance_data/{symbol}.csv'
        print(timeframe)
        filename = self.__get_file_name()

        since = self.__exchange.parse8601('2010-07-17T00:00:00Z')
        print(since)

        all_data = []
        while True:
            data = self.__get_binance_data(symbol, timeframe, since)
            if len(data) == 0:
                break
            all_data.extend(data)
            since = data[-1][0] + 1  # Update 'since' to get the next batch of data
        print(all_data)
        CsvHelper.save_binance_data_csv(all_data, file_name=filename)
        return all_data

    def __get_binance_data(self, symbol, timeframe='1d', since=None):
        """
        get data from binance api
        result: [timestamp, open, high, low, close, volume], where every row is key-value pair
        timeframe = ['1m' '1h' ,'1d', '1w']
        """
        limit = 500
        return self.__exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)

    def __get_currency_symbol(self):
        return self.__params.get('symbol', 'BTCUSDT')

    def __get_timeframe_alias(self):
        return self.__params.get('timeframe', '1d')

    def __get_file_name(self):
        return self.__params.get('file_name', 'btc_data_test.csv')
