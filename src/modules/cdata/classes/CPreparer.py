#
# src.services.CryptocurrencyDataPreparer.py
#
#
#
#
#
import numpy as np
import pandas as pd
from src.base.services.Settings import Settings
from src.modules.cdata.classes.CNormalizer import CNormalizer


class CPreparer:
    def __init__(self):
        self.__settings = Settings.get()

        # self.params['exchange_data_from_csv']  TODO already read table here, already downloaded
        # self.params['sequence_length']
        # self.params['feature_columns']

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
        # TODO make path to file not as CONSTANT
        df = self.__settings['handler_cdata']['save_csv_path']
        df = self.__convert_data_columns_into_date_format(df)
        df = self.__add_technical_indicators(df)
        df = self.__normalize_data(df)
        sets = self.__prepare_dataset(df)

        return sets

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
        # df['RSI'] = self.__calculate_rsi(df, 14)

        df['MACD'] = self.__calculate_ewm(df['Close'], 12) - self.__calculate_ewm(df['Close'], 26)
        df['Signal_Line'] = self.__calculate_ewm(df['MACD'], 9)
        df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']
        df = self.__add_bollinger_bands(df)
        df['MFI'] = self.__calculate_money_flow_index(df)
        df['RVI'] = self.__calculate_relative_volatility_index(df)

        return self.__drop_not_available_values(df)

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
        sma_period = self.__settings['ml_model']['cdata']['technical_indicators']['sma_period']
        std_dev_multiplier = self.__settings['ml_model']['cdata']['technical_indicators'][
            'standard_deviation_multiplier']

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

    def __calculate_ewm(self, df, period):
        return df.ewm(span=period, adjust=False).mean()

    def __calculate_money_flow_index(self, df):
        money_flow_ratio = self.__calculate_money_flow_ratio(df)
        return 100 - (100 / 1 + money_flow_ratio)

    def __calculate_money_flow_ratio(self, df):
        typical_price = (df['Close'] + df['Low'] + df['High']) / 3
        raw_money_flow = typical_price * df['Volume']
        positive_flow = raw_money_flow.where(typical_price > typical_price.shift(1), 0)
        negative_flow = raw_money_flow.where(typical_price < typical_price.shift(1), 0)
        positive_flow_sum = positive_flow.rolling(window=14).sum()
        negative_flow_sum = negative_flow.rolling(window=14).sum()
        return positive_flow_sum / negative_flow_sum

    def __calculate_relative_volatility_index(self, df):
        rvi_period = self.__settings['ml_model']['cdata']['technical_indicators']['relative_volatility_index_period']
        standard_deviation = df['Close'].rolling(window=rvi_period).std()
        mean_deviation = standard_deviation.rolling(window=rvi_period).mean()
        return standard_deviation / mean_deviation.where(mean_deviation != 0, np.nan)

    def __drop_not_available_values(self, df):
        return df.dropna(inplace=True)

    def __normalize_data(self, df):
        return CNormalizer(df).normalize()  #
        # TODO change to dynamic features then to tune hyper params




    ################ TODO NOT SET YET | NEED TO FIX FATAL ERRORS
    def __prepare_dataset(self, df):
        look_back = self.__settings['ml_model']['cdata']['datasets_params']['look_back']
        x, y = self.__create_dataset(self.__normalize_data(df).values, look_back)
        return self.__get_train_and_test_sets(df, {'x': x, 'y': y})


    def __get_train_and_test_sets(self, df, datasets, params=None):
        # df.dropna(inplace=True)
        # scaler_features = MinMaxScaler(feature_range=(0, 1))
        # df_scaled = scaler_features.fit_transform(df[params['features_columns']])
        # df_scaled = pd.DataFrame(df_scaled, columns=params['features_columns'])
        x = datasets['x']
        y = datasets['y']
        normalized_data = self.__normalize_data(df)
        set_size = self.__settings['ml_model']['cdata']['datasets_params']['train_set']['size']
        training_data_len = int(np.ceil(len(normalized_data) * set_size))
        # x_train, y_train = self.__create_dataset(normalized_data[:training_data_len])
        # x_test, y_test = self.__create_dataset(normalized_data[training_data_len:])
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
            x.append(df[i - sequence_length:i].to_numpy())
            y.append(df.iloc[i]['Close'])
        return np.array(x), np.array(y)
