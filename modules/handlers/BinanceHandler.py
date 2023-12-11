# BinanceHandler.py
#
#
# Binance date handler
# Getting and saving Binance data from Binance API to local csv file as a data storage
# use handle() to process the data from Binance API
#
#

import ccxt
from modules.handlers.DataHandler import DataHandler
from datetime import datetime, timedelta
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
        limit = self._get_limit()
        days = self._get_days_interval()

        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        path_to_file = f'../binance_data/{symbol}.csv'

        self._save_binance_data_csv(self._get_binance_data(
            symbol=symbol, timeframe=timeframe, limit=limit, days=days), file_name=self._get_file_name())


    def _get_binance_data(self, symbol, timeframe='1d', limit=1000, days=365):
        """
        get data from binance api
        result: [timestamp, open, high, low, close, volume], where every row is key-value pair
        timeframe = ['1m' '1h' ,'1d', '1w']
        """
        start_date = datetime.now() - timedelta(days=days)
        start_timestamp = int(start_date.timestamp() * 1000)
        return ccxt.binance().fetch_ohlcv(symbol, timeframe, since=start_timestamp, limit=limit)


    # def get_data(self):
    #     return ('data' in self.params) ? self.params['data']: None
    def _get_currency_symbol(self):
        return self.params.get('symbol', 'BTCUSDT')


    def _get_timeframe_alias(self):
        return self.params.get('timeframe', '1d')


    def _get_limit(self):
        return self.params.get('limit', 1000)


    def _get_days_interval(self):
        return self.params.get('days', 365)


    def _get_file_name(self):
        return self.params.get('file_name', 'base.csv')