#
# src.services.CryptocurrencyDataPreparer.py
#
#
#
#
#


import string
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from src.handlers.DataHandler import DataHandler


class CPreparer:
    def __init__(self, params: dict = None):
        if 'file_path' not in params or params is None:
            Exception()

        self.__params = params
        # self.params['exchange_data_from_csv']  TODO already read table here, already downloaded

    # def prepare_data(self):
    #     # TODO may be changed to DB
    #     df = pd.read_csv(self.params['backup_name'])
    #
    #     df = self.__add_technical_indicators(df)
    #     df['RSI'] = self.__calculate_rsi(14)
    #     df = self.__add_bollinger_bands(df)
    #
    #     dataset = self.__get_x_and_y_sets(df)
    #
    #     return dataset

    def prepare_data(self):
        df = self.__params['exchange_data_from_csv']
        df = self.__convert_data_columns_into_date_format(df)
        df = self.__add_technical_indicators(df)

        return df

    # def __get_crypto_exchange_data(self, backup_filename: str = None):
    #     filename = backup_filename if backup_filename else self.params['backup_name']
    #     return pd.read_csv(filename)

    def __convert_data_columns_into_date_format(self, df):
        df = pd.DataFrame(df)
        df.rename(columns={'Timestamp': 'Date'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'] / 1000, unit='s')
        return df

    # def __convert_data_columns_into_date_format(self):
    #     df = pd.DataFrame(self.__get_crypto_exchange_data())
    #     df.rename(columns={'Timestamp': 'Date'}, inplace=True)
    #     df['Date'] = pd.to_datetime(df['Date'] / 1000, unit='s')
    #
    #     data = df[['Close']]
    #     data = data.rename(columns={'Close': 'Actual_Close'})
    #     data['Target'] = df['Close'].rolling(2).apply(lambda x: x.iloc[1] > x.iloc[0])
    #     data['Date'] = df['Date']
    #     # return df.head()
    #     return data

    # def __calculate_rsi(self, window):
    #     delta = self.__convert_data_columns_into_date_format().diff()
    #     gain = ((delta.where(delta > 0, 0)).rolling(window=window).mean())
    #     loss = ((-delta.where(delta < 0, 0)).rolling(window=window).mean())
    #     RS = gain / loss
    #     return 100 - (100 / (1 + RS))

    def __calculate_rsi(self, df, window=14):
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        RS = gain / loss
        return 100 - (100 / (1 + RS))

    def __add_technical_indicators(self, df):
        df['RSI'] = self.__calculate_rsi(df, 14)
        ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
        ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = ema_12 - ema_26
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']
        df = self.__add_bollinger_bands(df)

        return df

    #
    # def __add_technical_indicators(self, df):
    #     # df['RSI'] = self.calculate_rsi(df['Close'], 14)
    #     ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
    #     ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
    #     df['MACD'] = ema_12 - ema_26
    #     df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    #     df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']
    #     return df

    # def __create_dataset(self, df, sequence_length):
    #     x, y = [], []
    #     for i in range(sequence_length, len(df)):
    #         x.append(df[i - sequence_length:i])
    #         y.append(df.iloc[i]['Close'])
    #     return np.array(x), np.array(y)

    #
    # def __get_x_and_y_sets(self, df):
    #     df.dropna(subset=['RSI'], inplace=True)
    #     if 'High' in df.columns and 'Low' in df.columns:
    #         df.drop(['High', 'Low'], axis=1, inplace=True)
    #     features_columns = ['Close', 'Volume', 'RSI', 'MACD', 'Signal_Line', 'MACD_Histogram']
    #
    #     sequence_length = 60
    #     # n_features = len(features_columns)
    #
    #     # scaler_price = MinMaxScaler(feature_range=(0, 1))
    #     scaler_features = MinMaxScaler(feature_range=(0, 1))
    #
    #     df_scaled = scaler_features.fit_transform(df[features_columns])
    #     df_scaled = pd.DataFrame(df_scaled, columns=features_columns)
    #     print(df_scaled)
    #
    #     training_data_len = int(np.ceil(len(df_scaled) * 0.8))
    #     # train_data_scaled = scaler_features.transform(df_scaled[features_columns])
    #     x_train, y_train = self.__create_dataset(df_scaled[:training_data_len], sequence_length)
    #     x_test, y_test = self.__create_dataset(df_scaled[training_data_len:], sequence_length)
    #
    #     return {
    #         'x_train': x_train,
    #         "y_train": y_train,
    #         'x_test': x_test,
    #         "y_test": y_test
    #     }

    def __add_bollinger_bands(self, df):
        sma_period = 20
        std_dev_multiplier = 2
        df['SMA'] = df['Close'].rolling(window=sma_period).mean()
        df['Upper_BB'] = df['SMA'] + df['Close'].rolling(window=sma_period).std() * std_dev_multiplier
        df['Lower_BB'] = df['SMA'] - df['Close'].rolling(window=sma_period).std() * std_dev_multiplier
        return df
    #
    # def __add_bollinger_bands(self, df):
    #     # set params for Bollinger Bands (BB)
    #     sma_period = 20  # using for 20-period SMA
    #     std_dev_multiplier = 2  # standart deviation
    #     crypto_data = self.__get_crypto_exchange_data()
    #
    #     df['Low'] = crypto_data['Low']
    #     df['High'] = crypto_data['High']
    #
    #     # calculate Bollinger Bands
    #     df['SMA'] = df['Close'].rolling(window=sma_period).mean()
    #     df['Upper_BB'] = df['SMA'] + df['Close'].rolling(window=sma_period).std() * std_dev_multiplier
    #     df['Lower_BB'] = df['SMA'] - df['Close'].rolling(window=sma_period).std() * std_dev_multiplier
    #
    #     # Calculate the Money Flow Index (MFI)
    #     typical_price = (df['Close'] + df['Low'] + df['High']) / 3
    #     raw_money_flow = typical_price * df['Volume']
    #     positive_flow = raw_money_flow.where(typical_price > typical_price.shift(1), 0)
    #     negative_flow = raw_money_flow.where(typical_price < typical_price.shift(1), 0)
    #
    #     # Calculate the money flow ratio
    #     positive_flow_sum = positive_flow.rolling(window=14).sum()
    #     negative_flow_sum = negative_flow.rolling(window=14).sum()
    #     money_flow_ratio = positive_flow_sum / negative_flow_sum
    #
    #     # Calculate the MFI
    #     mfi = 100 - (100 / (1 + money_flow_ratio))
    #     df['MFI'] = mfi
    #
    #     # set params for Relative Volatility Index (RVI)
    #     rvi_period = 10  # define the period for RVI, for example 10
    #
    #     # calculate Relative Volatility Index (RVI)
    #     standard_deviation = df['Close'].rolling(window=rvi_period).std()
    #     mean_deviation = standard_deviation.rolling(window=rvi_period).mean()
    #     df['RVI'] = standard_deviation / mean_deviation.where(mean_deviation != 0, np.nan)
    #
    #     # remove starting NA values after calculate indicators
    #     df.dropna(inplace=True)
