import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from src.base.classes.BaseNormalizer import BaseNormalizer
from src.base.enums.main.Modules import Modules
from src.base.services.MLConfig import MLConfig


class Normalizer(BaseNormalizer):
    """
    A class that normalizes financial data using MinMax scaling.

    This class scales the features of a provided DataFrame into a specified range, typically [0, 1],
    which is a common requirement for many machine learning algorithms.

    Attributes:
        __df (pd.DataFrame): The DataFrame containing the data to be normalized.
        __features_columns (list): The list of column names in __df that will be normalized.
        __scaler (MinMaxScaler): An instance of MinMaxScaler from scikit-learn used for normalization.

    Properties:
        scaler: Returns the instance of MinMaxScaler used for normalization.

    Methods:
        __init__(self, data_frame: pd.DataFrame): Initializes the Normalizer with a DataFrame.
        normalize(self) -> pd.DataFrame: Performs normalization on the feature columns and returns a new DataFrame.

    Usage:
        normalizer = Normalizer(data_frame)
        normalized_df = normalizer.normalize()
    """

    def __init__(self, data_frame: pd.DataFrame):
        """
        Initializes the Normalizer with a DataFrame and sets up the scaler.

        Parameters:
            data_frame (pd.DataFrame): The DataFrame containing the data to be normalized.
        """
        super().__init__(data_frame)
        self._data_frame.dropna(inplace=True)
        self.__features_columns = MLConfig(Modules.CData).features
        self.__scaler = MinMaxScaler(feature_range=(0, 1))

    @property
    def scaler(self):
        """Returns the instance of MinMaxScaler used for normalization."""
        return self.__scaler

    def normalize(self) -> pd.DataFrame:
        """
        Performs normalization on the feature columns of the DataFrame.

        This method applies MinMaxScaler to the specified feature columns of the DataFrame,
        scales them into the [0, 1] range, and returns a new DataFrame with the scaled values.

        Returns:
            pd.DataFrame: A DataFrame with normalized values for the feature columns.
        """
        df_scaled = self.__scaler.fit_transform(self._data_frame[self.__features_columns])
        return pd.DataFrame(df_scaled, columns=self.__features_columns)
