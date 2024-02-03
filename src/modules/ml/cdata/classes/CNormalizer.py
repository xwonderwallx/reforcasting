#
#
#
#
#
#
#
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from src.base.services.Config import Config


class CNormalizer:
    def __init__(self, data_frame):
        self.__df = data_frame
        self.__df.dropna(inplace=True)
        self.__settings = Config.get()
        self.__features_columns = self.__settings['ml_model']['cdata']['datasets_params']['features']
        self.__scaler = None

    def normalize(self):
        self.__scaler = MinMaxScaler(feature_range=(0, 1))
        df_scaled = self.__scaler.fit_transform(self.__df[self.__features_columns])
        return pd.DataFrame(df_scaled, columns=self.__features_columns)

    def get_scaler(self):
        return self.__scaler


