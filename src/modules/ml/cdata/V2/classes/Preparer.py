import numpy as np
import pandas as pd

from src.base.classes.BasePreparer import BasePreparer
from src.base.entities.Dataset import Dataset
from src.base.enums.main.Modules import Modules
from src.base.enums.ml.SetType import SetType
from src.base.helpers.LogHelper import LogHelper
from src.base.services.MLConfig import MLConfig
from src.base.services.Settings import Settings
from src.modules.ml.cdata.V2.helpers.CDataTechHelper import CDataTechHelper


class Preparer(BasePreparer):
    """
    A data preparation class that processes financial data for machine learning.

    The class extends BasePreparer and handles tasks such as converting date columns into a date
    format, adding technical indicators to the data, normalizing the data, and splitting it into
    training and testing sets.

    Attributes:
        __settings (Settings): Configuration settings for the preparer.
        __ml_helper (MLConfig): Machine learning configuration helper for the CData module.
        __df (pd.DataFrame): The dataframe containing financial data.

    Methods:
        __init__(self, df: pd.DataFrame): Initializes the Preparer instance with a dataframe.
        prepare(self): Prepares the data for machine learning by adding technical indicators,
                       normalizing, and splitting into sets.
        __add_technical_indicators(df: pd.DataFrame, window: int): Adds various technical indicators to the dataframe.
        __create_dataset(df, sequence_length): Creates sequences of data for the time-series prediction.
        __prepare_dataset(self, df): Prepares and splits the dataset into training and testing sets.
        __get_train_and_test_sets(self, df, datasets): Splits the data into training and test sets and returns a Dataset instance.

    Returns:
        A dictionary containing the prepared sets and the processed dataframe.
    """

    def __init__(self, df: pd.DataFrame, ml_module_name: Modules):
        """
        Initializes the Preparer instance with a dataframe of financial data.

        Args:
            df (pd.DataFrame): The dataframe to be prepared for machine learning.
        """
        super().__init__(df=df, ml_module_name=ml_module_name)
        self.__settings = Settings.get()
        self.__ml_helper = MLConfig(ml_module_name=Modules.CData)
        self.__df = df

    def prepare(self):
        """
        Prepares the financial data for machine learning.

        The method adds technical indicators to the dataframe, normalizes the data, and splits it
        into training and testing sets ready for machine learning models.

        Returns:
            dict: A dictionary containing 'sets', which is a Dataset instance with separated sets,
                  and 'df', which is the processed dataframe.
        """
        print("Preparing data...")

        df = self.__df
        try:
            if 'Date' in df.columns:
                # df['Date'] = pd.to_datetime(df['Date'])
                df = self._convert_data_columns_into_date_format(df)
            else:
                print("Warning: 'Date' column not found.")
        except Exception as e:
            print(f"Error during data preparation: {e}")
            return None

        df = Preparer.__add_technical_indicators(df)
        LogHelper.pretty_print(df, 'Preparing data...')
        df = self._normalize_data(df)

        prepared_data_obj = {
            'sets': self.__prepare_dataset(df),
            'df': df
        }

        LogHelper.pretty_print(prepared_data_obj, f'{LogHelper.default_log_label()} | prepared_data_obj')

        return prepared_data_obj

    @staticmethod
    def __add_technical_indicators(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
        close, macd, macd_histogram, mfi, rsi, rvi, signal_line = CDataTechHelper.define_special_features()

        # TODO Set this constant to the configuration file or change to dynamic params
        # TODO change CDataTechHelper to Builder pattern to make chain call and config from the config.json
        df[rsi] = CDataTechHelper.rsi(df, window)
        df[macd] = CDataTechHelper.ewm(df=df[close], period=12) - CDataTechHelper.ewm(df=df[close], period=26)
        df[signal_line] = CDataTechHelper.ewm(df[macd], period=9)
        df[macd_histogram] = df[macd] - df[signal_line]
        df = CDataTechHelper.add_bollinger_bands(df)

        # TODO fix error with money flow index
        # df[mfi] = CDataTechHelper.money_flow_index(df)

        df[rvi] = CDataTechHelper.rvi_period(Modules.CData)

        CDataTechHelper.drop_not_available_values(df)

        return df

    def __create_dataset(self, df, sequence_length=60):
        x, y = [], []
        for i in range(sequence_length, len(df)):
            x.append(df[i - sequence_length:i])
            y.append(df[i, 0])
        return np.array(x), np.array(y)

    def __prepare_dataset(self, df):
        look_back = self.__ml_helper.look_back
        x, y = self.__create_dataset(self._normalize_data(df).values, look_back)
        sets = self.__get_train_and_test_sets(df=df, datasets={'x': x, 'y': y})

        LogHelper.pretty_print(sets, f'{LogHelper.default_log_label()} | Prepared Dataset')

        return sets

    def __get_train_and_test_sets(self, df, datasets) -> Dataset:
        x = datasets['x']
        y = datasets['y']
        normalized_data = self._normalize_data(df)
        train_set_size = self.__ml_helper.train_set_size
        training_data_len = int(np.ceil(len(normalized_data) * train_set_size))

        separated_sets = Dataset(separated_sets={
            SetType.XTrain.value: x[:training_data_len],
            SetType.YTrain.value: y[:training_data_len],
            SetType.XTest.value: x[training_data_len:],
            SetType.YTest.value: y[training_data_len:]
        })

        LogHelper.pretty_print(separated_sets, f"{LogHelper.default_log_label() } | separated sets")
        LogHelper.pretty_print(self.__ml_helper.train_set_size, f"{LogHelper.default_log_label() } | self.__ml_helper.train_set_size")

        return separated_sets
