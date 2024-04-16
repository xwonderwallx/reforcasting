from src.base.enums.exchange.SourceMarket import SourceMarket
from src.base.helpers.CsvHelper import CsvHelper
from src.base.helpers.ExchangeDataHelper import ExchangeDataHelper
from src.base.services.Config import Config
from src.base.services.Timer import Timer
from src.modules.dc.cdata.handlers.BinanceHandler import BinanceHandler
from src.modules.dc.cdata.helpers.MarketHelper import MarketHelper


class Market:
    """
    A class responsible for handling market data operations for Binance trading pairs.

    This class provides functionalities to collect data from the Binance API, organize it,
    and save it to CSV files. It uses a specified handler to interface with the Binance API
    and utilizes a timer to track operation durations.

    Attributes:
        __handler (BinanceHandler): An instance of BinanceHandler to interact with the Binance API.
        __timer (Timer): An instance of Timer to measure operation durations.
        __config (Config): An instance of Config to access configuration settings.
        __trading_pairs (list): A list of trading pairs to collect data for, as specified in the configuration.
        __binance_data (list): A list of collected Binance data for the specified trading pairs.

    Properties:
        binance_data: Retrieves all collected data from the Binance API for different currencies.

    Methods:
        __init__(self, handler: BinanceHandler): Initializes the Market instance.
        save_binance_data_to_csv_file(): Saves the collected Binance data to a CSV file.
        __get_binance_handler_params_for_each_trading_pair(): Generates handler parameters for each trading pair.

    Raises:
        Exception: If any issue occurs during the initialization process.
    """

    def __init__(self, handler: BinanceHandler):
        """
        Initializes the Market instance with a BinanceHandler and sets up necessary attributes.

        Parameters:
            handler (BinanceHandler): A handler to interact with the Binance API.
        """
        self.__handler = handler
        self.__timer = Timer()
        self.__config = Config()
        self.__trading_pairs = ExchangeDataHelper.source_market_trading_pairs(source_market=SourceMarket.Binance)
        self.__binance_data = self.binance_data

    # TODO Finish the property . It is a skeleton right now | need to add a timeframe period
    # The full data from Binance of trading pairs from configuration
    @property
    def binance_data(self):
        """
        Retrieves all collected data from the Binance API for different currencies.

        This property orchestrates the collection of market data for each trading pair and returns
        a list containing the data for all specified pairs.

        Returns:
            list: A list of collected market data from Binance.
        """
        binance_handler_params = self.__get_binance_handler_params_for_each_trading_pair()
        all_collected_cdata = []

        self.__timer.refresh_timer()
        self.__timer.start(label='src.moduler.dc.cdata.classes.Market.binance_data')

        for params in binance_handler_params:
            inner_timer = Timer(f'{params}')
            inner_timer.start()

            binance_data = MarketHelper.execute_binance_data_collection(params=params)
            all_collected_cdata.append(binance_data)

            inner_timer.stop()
            print(inner_timer.info())

        self.__timer.stop()
        print(self.__timer.info())

        return all_collected_cdata

    def save_binance_data_to_csv_file(self):
        """
        Saves the collected Binance data to a CSV file specified in the configuration.

        This method checks if there is any collected data to save. If data is present,
        it is saved to a CSV file in the configured path. Otherwise, an informative message
        is printed.
        """
        self.__timer.refresh_timer()
        self.__timer.start(label='src.moduler.dc.cdata.classes.Market.save_binance_data_to_csv_file()')

        if self.__binance_data is not None:
            filepath = self.__config.exchange_data_path['exchange_data']
            print(f"{self.__binance_data} is not None")
            CsvHelper.save_binance_data_csv(data=self.__binance_data, file_name=f'{filepath}full_market_data.csv')
        else:
            print(f"No binance data was saved | {self.__binance_data}")

        self.__timer.stop()
        print(self.__timer.info())

    def __get_binance_handler_params_for_each_trading_pair(self):
        """
        Generates handler parameters for each trading pair as specified in the configuration.

        This method prepares the parameters required by the BinanceHandler to collect market data
        for each trading pair. It includes symbol, timeframe, and file name for saving data.

        Returns:
            list: A list of dictionaries containing handler parameters for each trading pair.
        """
        symbols_pairs = []

        self.__timer.refresh_timer()
        self.__timer.start(label='src.moduler.dc.cdata.classes.Market.__get_binance_handler_params_with_each_pair()')

        for pair in self.__trading_pairs:
            filepath = self.__config.exchange_data_path
            inner_timer = Timer('pair')
            inner_timer.start()
            symbols_pair = {
                'symbol': pair,
                'timeframe': '1d',
                'file_name': f'{filepath}{pair}.csv'
                # TODO set time interval here in the near future | i.e. year - two - three...
            }
            inner_timer.stop()
            print(symbols_pair)
            print(inner_timer.info())
            symbols_pairs.append(symbols_pair)

        self.__timer.stop()
        print(self.__timer.info())

        return symbols_pairs
