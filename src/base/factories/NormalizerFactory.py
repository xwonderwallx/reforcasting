import pandas as pd

from src.base.enums.main.Modules import Modules
from src.modules.ml.cdata.V2.classes.Normalizer import Normalizer as cNormalizer


class NormalizerFactory:
    """
    A factory class for creating normalizer instances specific to different machine learning modules.

    This class uses the Factory Method design pattern to abstract the creation process of normalizer
    instances. It decides which normalizer class to instantiate based on the provided machine learning
    module enum. This approach centralizes normalizer creation, facilitating easy management and expansion.

    Methods:
        create(ml_module: Modules, df: pd.DataFrame = None): A static method that creates and returns
                                                             an instance of a normalizer based on the specified
                                                             machine learning module.
    """

    @staticmethod
    def create(ml_module: Modules, df: pd.DataFrame = None):
        """
        Creates and returns an instance of a normalizer based on the specified machine learning module.

        This method checks the provided `ml_module` parameter against known modules and instantiates
        the corresponding normalizer class with the provided DataFrame `df` if applicable. The method
        can be extended to include additional machine learning modules and their associated normalizers.

        Parameters:
            ml_module (Modules): An enum value specifying the machine learning module for which
                                 the normalizer is being created.
            df (pd.DataFrame, optional): The DataFrame to be normalized by the created normalizer instance.
                                         Defaults to None.

        Returns:
            An instance of a normalizer class corresponding to the specified `ml_module`. Currently,
            supports `Modules.CData` for creating instances of `cNormalizer`.

        Raises:
            ValueError: If an unsupported `ml_module` is specified.

        Example:
            >>> normalizer = NormalizerFactory.create(Modules.CData, my_dataframe)
            >>> # Now `normalizer` is an instance of `cNormalizer` configured with `my_dataframe`.
        """
        if ml_module == Modules.CData:
            return cNormalizer(df)
        # Extend this conditional to include additional modules and their normalizers as needed.
        else:
            raise ValueError(f"Unsupported module: {ml_module}")
