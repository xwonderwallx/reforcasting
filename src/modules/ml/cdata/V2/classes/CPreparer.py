#
# src.services.CryptocurrencyDataPreparer.py
#
#
#
#
#
import numpy as np
import pandas as pd
from src.base.services.Config import Config
from src.modules.ml.cdata.classes.CNormalizer import CNormalizer


class CPreparer:
    def __init__(self, df):
        self.__settings = Config.get()
        self.__df = df

    def prepare_data(self):
        df = self.__df
        df = self.__convert_data_columns_into_date_format(df)
        df = self.__add_technical_indicators(df)
        df = self.__normalize_data(df)

        sets = self.__prepare_dataset(df)

        return {
            'sets': sets,
            'df': df
        }

    def __convert_data_columns_into_date_format(self, df):
        df = pd.DataFrame(df)
        df.rename(columns={'Timestamp': 'Date'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'] / 1000, unit='s')
        return df

    def __calculate_rsi(self, df, window=14):
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        RS = gain / loss
        return 100 - (100 / (1 + RS))

    def __add_technical_indicators(self, df):
        df['RSI'] = self.__calculate_rsi(df, 14)

        df['MACD'] = self.__calculate_ewm(df['Close'], 12) - self.__calculate_ewm(df['Close'], 26)
        df['Signal_Line'] = self.__calculate_ewm(df['MACD'], 9)
        df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']
        df = self.__add_bollinger_bands(df)
        df['MFI'] = self.__calculate_money_flow_index(df)
        df['RVI'] = self.__calculate_relative_volatility_index(df)

        self.__drop_not_available_values(df)
        return df

    def __add_bollinger_bands(self, df):
        sma_period = self.__settings['ml_model']['cdata']['technical_indicators']['sma_period']
        std_dev_multiplier = self.__settings['ml_model']['cdata']['technical_indicators'][
            'standard_deviation_multiplier']

        df['SMA'] = df['Close'].rolling(window=sma_period).mean()
        df['Upper_BB'] = df['SMA'] + df['Close'].rolling(window=sma_period).std() * std_dev_multiplier
        df['Lower_BB'] = df['SMA'] - df['Close'].rolling(window=sma_period).std() * std_dev_multiplier

        return df

    def __drop_not_available_values(self, df):
        df.dropna(inplace=True)

    def __normalize_data(self, df):
        print(df.columns)
        return CNormalizer(df).normalize()  #
        # TODO change to dynamic features then to tune hyper params

    def __prepare_dataset(self, df):
        look_back = self.__settings['ml_model']['cdata']['datasets_params']['look_back']
        x, y = self.__create_dataset(self.__normalize_data(df).values, look_back)
        return self.__get_train_and_test_sets(df, {'x': x, 'y': y})

    def __get_train_and_test_sets(self, df, datasets, params=None):
        x = datasets['x']
        y = datasets['y']
        normalized_data = self.__normalize_data(df)
        set_size = self.__settings['ml_model']['cdata']['datasets_params']['train_set']['size']
        training_data_len = int(np.ceil(len(normalized_data) * set_size))
        (x_train, x_test,
         y_train, y_test) = (
            x[:training_data_len], x[training_data_len:],
            y[:training_data_len], y[training_data_len:])

        return {
            'x_train': x_train,
            'y_train': y_train,
            'x_test': x_test,
            'y_test': y_test
        }

    def __create_dataset(self, df, sequence_length=60):
        x, y = [], []
        for i in range(sequence_length, len(df)):
            x.append(df[i - sequence_length:i])
            y.append(df[i, 0])
        return np.array(x), np.array(y)
