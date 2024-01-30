#
# src.services.CryptocurrencyDataPreparer.py
#
#
#
#
#
import numpy as np

from src.base.classes.IPreparer import IPreparer


class PDPreparer(IPreparer):
    def __init__(self, model, sets):
        super().__init__()
        self.__model = model
        self.__sets = sets

    def prepare_data(self):
        predicted_train_prices = self.__model.predict_proba(self.__sets['x_train'])
        y_train_direction = np.where(predicted_train_prices[:-1].flatten() < self.__sets['y_train'][1:], 1, 0)
        x_train_direction = np.where(self.__sets['x_train'][:-1])
        return {
            'x_train_direction': x_train_direction,
            'y_train_direction': y_train_direction
        }
