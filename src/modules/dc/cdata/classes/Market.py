from src.base.enums.SourceMarket import SourceMarket
from src.base.helpers.CsvHelper import CsvHelper
from src.base.helpers.ExchangeDataHelper import ExchangeDataHelper
from src.base.services.Config import Config
from src.base.services.Settings import Settings
from src.base.services.Timer import Timer
from src.modules.dc.cdata.handlers.BinanceHandler import BinanceHandler
from src.modules.dc.cdata.helpers.MarketHelper import MarketHelper


class Market:

    def __init__(self, handler: BinanceHandler):
        self.__handler = handler
        self.__timer = Timer()
        self.__settings = Settings.get()
        self.__trading_pairs = ExchangeDataHelper.source_market_trading_pairs(source_market=SourceMarket.Binance)
        self.__binance_data = self.binance_data
        self.__config = Config()

    # TODO Finish the property . It is a skeleton right now | need to add a timeframe period
    # The full data from Binance of trading pairs from configuration
    @property
    def binance_data(self):
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
