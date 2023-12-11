# ModelTrainer.py
# 
# 
# 
# 
# 
# 
# 
# 

import numpy as np
from sklearn.linear_model import LinearRegression
from modules.DataProcessor import DataProcessor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import logging


class ModelTrainer():
    
    def __init__(self, model, resource, logger=None):
        self.model = model
        self.data_processor = DataProcessor(resource)
        self.logger = logging.getLogger(__name__)
        
    def handle_train_data(self):
        train_data, test_data = self.data_processor.get_test_and_train_sets()
        
        self.logger.debug(f"Length of train_data: {len(train_data)}")
        self.logger.debug(f"Length of test_data: {len(test_data)}")
        self.logger.debug(f"train_data: \n{train_data}")
        if 'Date' not in train_data.columns or 'Date' not in test_data.columns:
            self.logger.error("Date column is missing after train-test split.")
            return None, None, None, None
        
        X_train = train_data.drop(['Close'], axis=1)
        y_train = train_data['Close']
        X_test = test_data.drop(['Close'], axis=1)
        y_test = test_data['Close']
        return X_train, y_train, X_test, y_test
        
    def train_model(self, x_train, y_train):
        non_numerical_columns = x_train.select_dtypes(include=['datetime', 'object']).columns
        x_train_numerical = x_train.drop(columns=non_numerical_columns)

        scaler = MinMaxScaler()
        x_train_scaled = scaler.fit_transform(x_train_numerical)
        y_train_scaled = y_train.ravel()  

        self.model.fit(x_train_scaled, y_train_scaled)
        return self.model, scaler
    
    
    def predict(self, X_test, scaler):

        non_numerical_columns = X_test.select_dtypes(include=['datetime', 'object']).columns
        X_test_numerical = X_test.drop(columns=non_numerical_columns)
        X_test_scaled = scaler.transform(X_test_numerical)
        
        predictions_scaled = self.model.predict(X_test_scaled)
        predictions = predictions_scaled  # If scaling is applied to y, inverse transform is needed
        return predictions