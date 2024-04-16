from src.base.enums.exchange.SourceMarket import SourceMarket
from src.base.services.Config import Config
from src.base.services.Settings import Settings


class ExchangeDataHelper:
    """
    src.base.helpers.ExchangeDataHelper.py


    Description

      ExchangeDataHelper is a utility class designed for managing and accessing exchange data
      within a financial or cryptocurrency trading application.
      It provides methods to retrieve trading pairs from a specified source market
      and generate paths to the data files for these trading pairs. This
      class is particularly useful for applications that need to interface with different cryptocurrency exchanges and
      require a systematic way to access trading data stored in files.

    Methods

      source_market_trading_pairs(source_market: SourceMarket = SourceMarket.Binance):
              Static method that returns trading pairs available in the specified source market.
              By default, it uses Binance as the source market. This method reads the configuration to determine
              the trading pairs associated with the given market.
          Parameters:
              source_market (SourceMarket): An enumeration value representing the source market
              from which to retrieve trading pairs. Defaults to SourceMarket.Binance.
          Returns: A list of trading pairs (strings) available in the specified source market.

      paths_to_trading_pairs_exchange_data(source_market: SourceMarket = SourceMarket.Binance):
              Static method that generates and returns the file paths for exchange data corresponding to
              each trading pair for the specified source market. By default, it targets the Binance market.
              It leverages the source_market_trading_pairs method to get trading pairs and constructs the file paths
              where their data is stored.
          Parameters:
              source_market (SourceMarket): An enumeration value indicating the source market
              for which to generate data paths. Defaults to SourceMarket.Binance.
          Returns: A list of file paths (strings) for the exchange data of each trading pair
          in the specified source market.

      path_to_exchange_data_folder():
              Static method that retrieves the base path to the folder where exchange data files are stored.
              This path is defined in the application's settings configuration.
          Returns: A string representing the path to the exchange data folder as defined in the application's settings.
    """
    @staticmethod
    def source_market_trading_pairs(source_market: SourceMarket = SourceMarket.Binance):
        print(source_market)
        return Config().trading_pairs[source_market]

    @staticmethod
    def paths_to_trading_pairs_exchange_data(source_market: SourceMarket = SourceMarket.Binance):
        trading_pairs = ExchangeDataHelper.source_market_trading_pairs(source_market=source_market.value)
        exchange_data_folder_path = ExchangeDataHelper.path_to_exchange_data_folder()
        paths = []
        for tpair in trading_pairs:
            paths.append(f"{exchange_data_folder_path}{tpair}.csv")
        return paths

    @staticmethod
    def path_to_exchange_data_folder():
        return Config().exchange_data_path
