from array import array

import pandas as pd

from src.base.enums.exchange.ExchangeTableColumn import ExchangeTableColumn
from src.base.enums.main.Modules import Modules
from src.base.factories.NormalizerFactory import NormalizerFactory
from src.base.helpers.LogHelper import LogHelper


class BasePreparer:
    """
    A base class for preparing data for machine learning modules.

    This class provides foundational methods for data preprocessing such as converting date columns
    into a standardized date format and normalizing data using the appropriate normalizer for the given
    machine learning module.

    Attributes:
        __df (pd.DataFrame): The dataframe containing raw data to be prepared.
        __ml_module_name (Modules): The machine learning module for which the data is being prepared.

    Methods:
        __init__(self, df: pd.DataFrame, ml_module_name: Modules): Constructs the BasePreparer instance with data and module information.
        prepare(self): Placeholder for the prepare method to be implemented by subclasses.
        _convert_data_columns_into_date_format(self, df): Converts columns with timestamp data to datetime objects.
        _normalize_data(self, df): Normalizes the data using the NormalizerFactory based on the module name.
    """

    def __init__(self, df: pd.DataFrame, ml_module_name: Modules):
        """
        Initializes the BasePreparer with a dataframe and a machine learning module name.

        Args:
            df (pd.DataFrame): The dataframe containing the data to be prepared.
            ml_module_name (Modules): The machine learning module for which the data is being prepared.
        """
        self.__df = df
        self.__ml_module_name = ml_module_name

    def prepare(self):
        """
        A placeholder method that should be overridden by subclasses to prepare the data.

        Returns:
            bool: Always returns False. Subclasses should return prepared data.
        """
        return False

    def _convert_data_columns_into_date_format(self, df):
        """
        Converts columns with timestamp data to datetime objects.

        Args:
            df (pd.DataFrame): The dataframe whose timestamp columns are to be converted.

        Returns:
            pd.DataFrame: The dataframe with the timestamp columns converted to datetime objects.
        """
        df = pd.DataFrame(df)
        df.rename(columns={
            ExchangeTableColumn.Timestamp: ExchangeTableColumn.Date
        }, inplace=True)
        df[ExchangeTableColumn.Date.value] = pd.to_datetime(df[ExchangeTableColumn.Date.value] / 1000, unit='s')
        return df

    def _normalize_data(self, df):
        """
        Normalizes the data using the NormalizerFactory based on the machine learning module name.

        Args:
            df (pd.DataFrame): The dataframe to be normalized.

        Returns:
            pd.DataFrame: The normalized dataframe.
        """
        normalized_data = NormalizerFactory.create(ml_module=self.__ml_module_name, df=df).normalize()
        LogHelper.pretty_print(df, 'Normalized Data')
        return normalized_data
