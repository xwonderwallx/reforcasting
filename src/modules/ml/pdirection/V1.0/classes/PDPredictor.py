#
#
#
# /
#
#
#
import numpy as np

from src.base.services.Config import Config
from src.modules.ml.cdata.classes.CNormalizer import CNormalizer


class PDPredictor:
    def __init__(self, trained_model, sets):
        self.__trained_model = trained_model
        self.__settings = Config.get()
        self.__sets = sets

    def predict(self):
        predicted_prices = self.__trained_model.predict(self.__sets['x_test'])
        y_test_direction = self.__get_test_set(predicted_prices)
        x_test_direction = self.__sets['x_test'][1:]

        return {
            'predicted_price': predicted_prices,
            'y_test_direction': y_test_direction,
            'x_test_direction': x_test_direction
        }

    def __get_test_set(self, predicted_prices):
        return np.where(predicted_prices[:-1].flatten() < self.__sets['y_test'][1:], 1, 0)