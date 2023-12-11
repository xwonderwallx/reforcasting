# DataPreparator.py
# prepare data before processing
#
#
# Handling loading, cleaning, scaling, and other data transformations
# needed to prepare for model training
#
#

import pandas as pd
from sklearn.model_selection import train_test_split


class DataPreparator():
    
    def __init__(self, resource):
        self.resource = resource

    def load_data(self):
        data = pd.read_csv(self.resource)
        # Convert 'Timestamp' to datetime here instead of in prepare_data
        data['Date'] = pd.to_datetime(data['Timestamp'], unit='ms')
        return data

    def split_to_training_and_testing_sets(self, data_to_train):
        train_data, test_data = train_test_split(
            data_to_train, test_size=0.2, random_state=42)
        return train_data, test_data

    def split_train_test(self, data):
        test_size = 0.2  # 20% for testing
        test_rows = int(len(data) * test_size)
        train_rows = len(data) - test_rows

        # Ensure test set has exactly 200 rows
        if test_rows != 200:
            # Adjust the number of training rows to compensate
            train_rows = len(data) - 200
            test_rows = 200

        train_data = data.head(train_rows)
        test_data = data.tail(test_rows)
        
        return train_data, test_data
    
    
    def add_time_features(self, df):
        df['day_of_week'] = df['Date'].dt.dayofweek
        df['day_of_month'] = df['Date'].dt.day
        df['month_of_year'] = df['Date'].dt.month
        return df


    def add_lagged_features(self, df, number_of_lags):
        for lag in range(1, number_of_lags + 1):
            df[f'lag_{lag}'] = df['Close'].shift(lag)
        return df


    def add_rolling_window_features(self, df, window_size):
        df[f'rolling_mean_{window_size}'] = df['Close'].rolling(window=window_size).mean()
        df[f'rolling_std_{window_size}'] = df['Close'].rolling(window=window_size).std()
        return df

    def prepare_data(self, data):
        data = self.load_data()
        data['Date'] = pd.to_datetime(data['Timestamp'], unit='ms')
        data = self.add_time_features(data)
        data = self.add_lagged_features(data, number_of_lags=3)
        data = self.add_rolling_window_features(data, window_size=7)
        data = data.dropna()
        return data
