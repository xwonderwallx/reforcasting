#
#
#
#
#
#
#
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from src.base.services.Settings import Settings


class CNormalizer:
    def __init__(self, data_frame):
        self.__df = data_frame.dropna(inplace=True)
        self.__settings = Settings.get()
        self.__features_columns = self.__settings['ml_model']['cdata']['sets_params']['features']

    def normalize(self):
        return self.__normalize_features()

    @staticmethod
    def scale():
        return MinMaxScaler(feature_range=(0, 1))

    def __normalize_features(self):
        df_scaled = CNormalizer.scale().fit_transform(self.__df[self.__features_columns])
        return pd.DataFrame(df_scaled, columns=self.__features_columns)

