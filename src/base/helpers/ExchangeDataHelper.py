from src.base.enums.SourceMarket import SourceMarket
from src.base.services.Config import Config


class ExchangeDataHelper:
    @staticmethod
    def source_market_trading_pairs(source_market: SourceMarket = SourceMarket.Binance):
        return Config.get()['configuration']['exchange_data']['trading_pairs'][source_market]

    @staticmethod
    def paths_to_trading_pairs_exchange_data(source_market: SourceMarket = SourceMarket.Binance):
        trading_pairs = ExchangeDataHelper.source_market_trading_pairs(source_market=source_market)
        exchange_data_folder_path = ExchangeDataHelper.path_to_exchange_data_folder()
        paths = []
        for tpair in trading_pairs:
            paths.append(f"{exchange_data_folder_path}{tpair}.csv")
        return paths

    @staticmethod
    def path_to_exchange_data_folder():
        return Config.get()['configuration']['paths']['exchange_data']
