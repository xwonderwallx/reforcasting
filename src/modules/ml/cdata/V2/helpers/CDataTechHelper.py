import numpy as np
import pandas as pd

from src.base.enums.exchange.ExchangeTableColumn import ExchangeTableColumn
from src.base.enums.main.Modules import Modules
from src.base.enums.ml.SpecialFeature import SpecialFeature
from src.base.services.MLConfig import MLConfig


class CDataTechHelper:
    @staticmethod
    def rsi(df, window=14):
        close = ExchangeTableColumn.Close.value
        delta = df[close].diff()

        gain = CDataTechHelper.gain(delta, window)
        loss = CDataTechHelper.loss(delta, window)
        rs = CDataTechHelper.rs(gain, loss)

        return 100 - (100 / (1 + rs))

    @staticmethod
    def rs(gain, loss):
        return gain / loss

    @staticmethod
    def loss(delta, window):
        return (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    @staticmethod
    def gain(delta, window):
        return (delta.where(delta > 0, 0)).rolling(window=window).mean()

    @staticmethod
    def sma_period(ml_config: MLConfig):
        return ml_config.tech_indicators['sma_period']

    @staticmethod
    def std_dev_multiplier(ml_config: MLConfig):
        return ml_config.tech_indicators['standard_deviation_multiplier']

    @staticmethod
    def add_bollinger_bands(df):
        ml_config = MLConfig(ml_module_name=Modules.CData)
        sma_period = CDataTechHelper.sma_period(ml_config=ml_config)
        std_dev_multiplier = CDataTechHelper.std_dev_multiplier(ml_config=ml_config)

        close = ExchangeTableColumn.Close.value
        sma = SpecialFeature.SMA.value
        upper_bb = SpecialFeature.Upper_BB.value
        lower_bb = SpecialFeature.Lower_BB.value

        df[sma] = df[close].rolling(window=sma_period).mean()
        df[upper_bb] = df[sma] + df[close].rolling(window=sma_period).std() * std_dev_multiplier
        df[lower_bb] = df[sma] - df[close].rolling(window=sma_period).std() * std_dev_multiplier

        return df

    @staticmethod
    def drop_not_available_values(df) -> None:
        df.dropna(inplace=True)

    @staticmethod
    def ewm(df: pd.DataFrame, period):
        return df.ewm(span=period, adjust=False).mean()

    @staticmethod
    def money_flow_index(df: pd.DataFrame):
        money_flow_ratio = CDataTechHelper.money_flow_index(df)
        return 100 - (100 / 1 + money_flow_ratio)

    @staticmethod
    def money_flow_ratio(df, window=14):
        close = ExchangeTableColumn.Close.value
        low = ExchangeTableColumn.Low.value
        high = ExchangeTableColumn.High.value
        volume = ExchangeTableColumn.Volume.value

        typical_price = CDataTechHelper.typical_price(df=df, close=close, low=low, high=high, columns_amount=3)
        positive_flow_sum = CDataTechHelper.positive_money_flow(df=df, typical_price=typical_price,
                                                                volume=volume).rolling(window=window).sum()
        negative_flow_sum = CDataTechHelper.negative_money_flow(df=df, typical_price=typical_price,
                                                                volume=volume).rolling(window=window).sum()
        return positive_flow_sum / negative_flow_sum

    @staticmethod
    def typical_price(df: pd.DataFrame, close, low, high, columns_amount):
        return (df[close] + df[low] + df[high]) / columns_amount

    @staticmethod
    def positive_money_flow(df: pd.DataFrame, typical_price, volume):
        return CDataTechHelper.raw_money_flow(df=df, typical_price=typical_price, volume=volume).where(
            typical_price > typical_price.shift(1), 0)

    @staticmethod
    def negative_money_flow(df: pd.DataFrame, typical_price, volume):
        return CDataTechHelper.raw_money_flow(df=df, typical_price=typical_price, volume=volume).where(
            typical_price < typical_price.shift(1), 0)

    @staticmethod
    def raw_money_flow(df: pd.DataFrame, typical_price, volume):
        return typical_price * df[volume]

    @staticmethod
    def relative_volatility_index(df: pd.DataFrame, ml_module_name: Modules):
        rvi_period = CDataTechHelper.rvi_period(ml_module_name=ml_module_name)
        standard_deviation = CDataTechHelper.standard_deviation(df, rvi_period)
        mean_deviation = CDataTechHelper.mean_deviation(rvi_period, standard_deviation)
        return standard_deviation / mean_deviation.where(mean_deviation != 0, np.nan)

    @staticmethod
    def mean_deviation(rvi_period, standard_deviation):
        return standard_deviation.rolling(window=rvi_period).mean()

    @staticmethod
    def standard_deviation(df, rvi_period):
        return df['Close'].rolling(window=rvi_period).std()

    @staticmethod
    def rvi_period(ml_module_name: Modules):
        return MLConfig(ml_module_name=ml_module_name).tech_indicators['relative_volatility_index_period']

    @staticmethod
    def define_special_features():
        rsi = SpecialFeature.RSI.value
        macd = SpecialFeature.MACD.value
        signal_line = SpecialFeature.Signal_Line.value
        macd_histogram = SpecialFeature.MACD_Histogram.value
        mfi = SpecialFeature.MFI.value
        rvi = SpecialFeature.RVI.value
        close = ExchangeTableColumn.Close.value
        return close, macd, macd_histogram, mfi, rsi, rvi, signal_line
