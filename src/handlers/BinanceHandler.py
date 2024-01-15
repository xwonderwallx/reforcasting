# BinanceHandler.py
#
#
# Binance date handler
# Getting and saving Binance data from Binance API to local csv file as a local data storage
# use handle() to process the data from Binance API
#
#

import ccxt
from src.handlers.DataHandler import DataHandler
import csv


class BinanceHandler(DataHandler):

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
        self.params = params
        self.exchange = ccxt.binance()

    # from abstract DataHandler.php
    def handle(self):
        self._get_and_save_binance_data()

    def _save_binance_data_csv(self, data, file_name):
        with open(file_name, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Timestamp', 'Open', 'High',
                             'Low', 'Close', 'Volume'])
            for candle in data:
                timestamp, open_price, high, low, close, volume = candle
                writer.writerow(
                    [timestamp, open_price, high, low, close, volume])

    def _get_and_save_binance_data(self):
        # # TODO: markets for rate
        # # TODO: set format of date : array({day: d, rate: r}, {}, {}, {}, {})
        symbol = self._get_currency_symbol()
        timeframe = self._get_timeframe_alias()
        # url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        # path_to_file = f'../binance_data/{symbol}.csv'

        since = self.exchange.parse8601('2010-07-17T00:00:00Z')

        all_data = []
        while True:
            data = self._get_binance_data(symbol, timeframe, since)
            if len(data) == 0:
                break
            all_data.extend(data)
            since = data[-1][0] + 1  # Update 'since' to get the next batch of data

        self._save_binance_data_csv(all_data, file_name=self._get_file_name())

    def _get_binance_data(self, symbol, timeframe='1d', since=None):
        """
        get data from binance api
        result: [timestamp, open, high, low, close, volume], where every row is key-value pair
        timeframe = ['1m' '1h' ,'1d', '1w']
        """
        limit = 500
        return self.exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)

    def _get_currency_symbol(self):
        return self.params.get('symbol', 'BTCUSDT')

    def _get_timeframe_alias(self):
        return self.params.get('timeframe', '1d')

    def _get_file_name(self):
        return self.params.get('file_name', 'base.csv')
