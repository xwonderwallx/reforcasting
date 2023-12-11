# DataProcessor.py
# 
# 
# 
# 
# 
# 
# 

import modules.DataPreparator
import modules.DataAnalyzer


class DataProcessor():
    
    def __init__(self, resource):
        self.resource = resource
        self.preparator = DataPreparator(resource)
        self.analyzer = DataAnalyzer(resource)

    def prepare_data(self):
        data = self.preparator._load_data()
        train_data, test_data = self.preparator.split_train_test(data)
        return train_data, test_data
        
    def analyze_data(self):
        self.analyzer.patterns_analysis()
        self.analyzer.volume_analysis()
        # TODO: perform other analysis
    
    def preprocess_for_model(self, data):
        scaler, scaled_data = self.analyzer.scaling_data(data, 'file_path.csv')
        preprocessed_data = self.analyzer.preprocess_data(data, 'file_path.csv')
        return scaler, scaled_data, preprocessed_data
    
    def run():
        pass
