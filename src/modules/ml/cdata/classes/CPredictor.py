#
#
#
# /
#
#
#

from src.base.services.Config import Config
from src.modules.ml.cdata.classes.CNormalizer import CNormalizer


class CPredictor:
    def __init__(self, trained_model, sets, df):
        self.__trained_model = trained_model
        self.__settings = Config.get()
        self.__sets = sets
        self.__df = df
        self.__normalizer = CNormalizer(df)

    def predict(self):
        x_test = self.__sets['x_test']
        y_test = self.__sets['y_test']

        self.__normalizer.normalize()
        scaler = self.__normalizer.get_scaler()

        predicted = self.__trained_model.predict(x_test)
        predicted_prices = scaler.inverse_transform(predicted)
        real_values = scaler.inverse_transform(y_test.reshape(-1, 1))

        return {
            'predicted_price': predicted_prices,
            'real_values': real_values
        }

    # def get_predictions_as_dataframe(self):
    #     pd.DataFrame(dataframe_column)
    #

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