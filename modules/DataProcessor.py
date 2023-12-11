# DataProcessor.py
# 
# 
# 
# 
# 
# 
# 

from modules.DataPreparator import DataPreparator
from modules.DataAnalyzer import DataAnalyzer
from sklearn.feature_selection import f_regression
from sklearn.feature_selection import SelectKBest
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import logging


class DataProcessor():
    
    def __init__(self, resource):
        self.resource = resource
        self.preparator = DataPreparator(resource)
        self.analyzer = DataAnalyzer(resource)
        self.data = self.preparator.load_data()
        self.logger = logging.getLogger(__name__)
        if self.data is None:
            throw("Data loading failed.")


    def get_test_and_train_sets(self):
        train_data, test_data = self.preparator.split_train_test(self.data)
        self.logger.debug(f'\ntrain_data, test_data: \n{train_data}\n{test_data}')
        return train_data, test_data
        
        
    def get_analyzed_data(self):
        prepared_data = self.preparator.prepare_data(self.data)
        prepared_data = self.analyzer.add_technical_indicators(prepared_data)
        prepared_data = self.analyzer.macd(prepared_data)
        prepared_data = self.analyzer.rsi(prepared_data)
        self.logger.debug(f'\nprepared_data: \n{prepared_data}')
        # TODO: perform other analysis
        return prepared_data
    
    
    # def preprocess_for_model(self, data):
    #     scaler, scaled_data = self.analyzer.scaling_data(data, 'file_path.csv')
    #     preprocessed_data = self.analyzer.preprocess_data(data, 'file_path.csv')
    #     return scaler, scaled_data, preprocessed_data
    
    
    def process(self):    
        prepared_data = self.get_analyzed_data()
        # returns = data['Close'].pct_change().dropna()
        # garch_model = data_analyzer.fit_garch_model(returns)
        train_data, test_data = self.preparator.split_train_test(prepared_data)
        self.logger.debug(f'\ntrain_data, test_data: \n{train_data}\n{test_data}')
        return  train_data, test_data
    
    
    def get_data(self):
        return self.data
