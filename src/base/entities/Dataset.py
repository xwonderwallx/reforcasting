from src.base.enums.ml.SetType import SetType
from src.base.helpers.LogHelper import LogHelper


class Dataset:
    """
    A class to manage datasets split into training and testing sets, including features and labels.

    This class is designed to store and provide easy access to the separated parts of a dataset,
    specifically the training and testing sets for both features (X) and labels (Y). It ensures
    that the dataset is correctly formatted upon initialization.

    Attributes:
        __sets (dict): A dictionary containing the separated dataset parts, keyed by set type.
        __keys (dict_keys): The keys from the separated_sets dictionary indicating the available set types.

    Properties:
        x_train: Returns the training features from the dataset.
        y_train: Returns the training labels from the dataset.
        x_test: Returns the testing features from the dataset.
        y_test: Returns the testing labels from the dataset.

    Methods:
        __init__(self, separated_sets: dict): Initializes the Dataset instance with separated dataset sets.
        __check_permissions(self): Checks if all required dataset parts are present and correctly formatted.

    Raises:
        Exception: If the dataset is incorrectly formatted or missing required parts.
    """

    def __init__(self, separated_sets: dict):
        """
        Initializes a Dataset instance with separated dataset sets.

        Parameters:
            separated_sets (dict): A dictionary containing the separated parts of the dataset,
                                   keyed by enums from SetType. Expected keys are XTrain, YTrain,
                                   XTest, and YTest, corresponding to training features, training labels,
                                   testing features, and testing labels, respectively.

        Raises:
            Exception: If the dataset is missing any of the required parts or is incorrectly formatted.
        """
        self.__sets = separated_sets
        # self.__keys = separated_sets.keys()

        debug = {
            'sets': separated_sets,
            # 'keys': self.__keys
        }

        LogHelper.pretty_print(debug, f'{LogHelper.default_log_label()} | init params')

        if self.__check_permissions() is False:
            raise Exception("The dataset is incorrectly formatted.")

    @property
    def x_train(self):
        """Returns the training features from the dataset."""
        print(self.__sets[SetType.XTrain.value], f'{LogHelper.default_log_label()} | x_train')
        return self.__sets[SetType.XTrain.value]

    @property
    def y_train(self):
        """Returns the training labels from the dataset."""
        print(self.__sets[SetType.YTrain.value], f'{LogHelper.default_log_label()} | x_train')
        return self.__sets[SetType.YTrain.value]

    @property
    def x_test(self):
        """Returns the testing features from the dataset."""
        print(self.__sets[SetType.XTest.value], f'{LogHelper.default_log_label()} | x_train')
        return self.__sets[SetType.XTest.value]

    @property
    def y_test(self):
        """Returns the testing labels from the dataset."""
        print(self.__sets[SetType.YTest.value], f'{LogHelper.default_log_label()} | x_train')
        return self.__sets[SetType.YTest.value]

    def __check_permissions(self):
        """
        Checks if all required dataset parts are present and correctly formatted.

        This method verifies the presence of all required keys in the dataset dictionary,
        ensuring that the dataset includes both training and testing sets for features and labels.

        Returns:
            bool: True if the dataset is correctly formatted, False otherwise.
        """
        required_keys = [SetType.XTrain.value, SetType.YTrain.value, SetType.XTest.value, SetType.YTest.value]
        return all(key in self.__sets for key in required_keys)
