import ccxt
from src.base.handlers.IHandler import IHandler
from src.base.helpers.CsvHelper import CsvHelper


class BinanceHandler(IHandler):
    """
    A class for handling the retrieval and storage of market data from the Binance API.

    This handler connects to the Binance API, fetches market data for a given cryptocurrency pair,
    and timeframe, then saves the data to a local CSV file. It is designed to be used with a
    dictionary of parameters that specify the details of the data to be fetched and stored.

    Attributes:
        __params (dict): A dictionary containing parameters for data handling.
        __exchange (ccxt.binance): An instance of the ccxt Binance exchange class,
                                   used to interact with the Binance API.

    Methods:
        __init__(self, params=None): Initializes the handler with given parameters.
        exchange (property): Returns the ccxt Binance exchange instance.
        handle(self): The main method to be called to fetch and save data.
        __get_and_save_binance_data(self): Retrieves data from Binance and saves it to a CSV file.
        __get_binance_data(self, symbol, timeframe='1d', since=None): Fetches market data from Binance API.
        __get_currency_symbol(self): Retrieves the currency symbol from the parameters.
        __get_timeframe_alias(self): Retrieves the timeframe alias from the parameters.
        __get_file_name(self): Retrieves the file name from the parameters for saving the data.
    """

    def __init__(self, params=None):
        """
        Initializes the BinanceHandler with the provided parameters.

        Args:
            params (dict, optional): Parameters for handling data which can include 'data',
                                     'symbol', 'timeframe', 'limit', and 'days'. Defaults to None.
        """
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

    @property
    def exchange(self):
        """Returns the ccxt Binance exchange instance."""
        return self.__exchange

    def handle(self):
        """
        The main method to be called to fetch and save data.

        Returns:
            list: The market data retrieved from the Binance API and saved to CSV.
        """
        return self.__get_and_save_binance_data()

    def __get_and_save_binance_data(self):
        symbol = self.__get_currency_symbol()
        timeframe = self.__get_timeframe_alias()
        filename = self.__get_file_name()
        since = self.__exchange.parse8601('2010-07-17T00:00:00Z')

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
