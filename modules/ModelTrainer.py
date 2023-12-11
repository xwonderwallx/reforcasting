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


class ModelTrainer():
    
    def __init__(self, model):
        self.model = model
        
    def train_model(self, x_train, y_train):
        self.model.fit(x_train, y_train)
        return self.model