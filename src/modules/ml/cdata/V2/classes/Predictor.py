import pandas as pd

from src.base.classes.BasePredictor import BasePredictor
from src.base.services.Settings import Settings
from src.modules.ml.cdata.V2.classes.Normalizer import Normalizer


class Predictor(BasePredictor):
    def __init__(self, trained_model, sets, data_frame: pd.DataFrame):
        super().__init__()
        self.__trained_model = trained_model
        self.__settings = Settings.get()
        self.__sets = sets
        self.__data_frame = data_frame
        self.__normalizer = Normalizer(data_frame=data_frame)

    def predict(self, params=None):
        x_test = self.__sets['x_test']
        y_test = self.__sets['y_test']

        self.__normalizer.normalize()
        scaler = self.__normalizer.scaler

        predicted = self.__trained_model.predict(x_test)
        predicted_prices = scaler.inverse_transform(predicted)
        real_values = scaler.inverse_transform(y_test.reshape(-1, 1))

        return {
            'predicted_price': predicted_prices,
            'real_values': real_values
        }

    # # Calculate evaluation metrics
    # mse = mean_squared_error(real_values, predicted_prices)
    # mae = mean_absolute_error(real_values, predicted_prices)
    # r2 = r2_score(real_values, predicted_prices)
    #
    # # Prepare data for visualization
    # visualize = {
    #     'real': real_values.flatten(),
    #     'predicted': predicted_prices.flatten()
    # }
