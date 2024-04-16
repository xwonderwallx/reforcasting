import pandas as pd


class BaseNormalizer:
    def __init__(self, data_frame: pd.DataFrame):
        self._data_frame = data_frame

    def normalize(self) -> pd.DataFrame:
        pass
