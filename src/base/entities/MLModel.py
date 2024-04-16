from src.base.enums.main.Modules import Modules
from src.base.services.MLConfig import MLConfig


class MLModel:
    """
    A class representing a machine learning model configuration and setup.

    This class encapsulates the machine learning model's configuration by interfacing
    with the MLConfig class. It provides easy access to model configurations, hyperparameters,
    and dataset parameters required for initializing and training machine learning models.

    Attributes:
        __ml_config (MLConfig): An instance of the MLConfig class containing the configuration
                                for the specified machine learning module.

    Properties:
        ml_module_name: Retrieves the name of the current machine learning module from MLConfig.
        hyper_parameters: Accesses the hyperparameters for the machine learning model.
        model_type: Gets the type of the model as configured in MLConfig.
        features: Lists the features to be used by the machine learning model.
        epochs: The number of epochs for training the model.
        batch_size: The batch size for training the model.
        look_back: The look-back period to be used by the model for sequences.
        callbacks: Retrieves the configured callbacks for model training.
        datasets_params: Accesses dataset parameters like splitting ratios.
        test_set_size: The size ratio of the test dataset.
        train_set_size: The size ratio of the training dataset.
        sequence_default_length: The default sequence length for model input.

    Methods:
        __init__(self, ml_module_name: Modules): Initializes the MLModel instance
                                                with the specified machine learning module name.
    """

    def __init__(self, ml_module_name: Modules):
        self.__ml_config = MLConfig(ml_module_name=ml_module_name)

    @property
    def ml_module_name(self):
        return self.__ml_config.current_module_settings

    @property
    def hyper_parameters(self):
        return self.__ml_config.hyper_parameters

    @property
    def model_type(self):
        return self.__ml_config.model_type

    @property
    def features(self):
        return self.__ml_config.features

    @property
    def epochs(self):
        return self.epochs

    @property
    def batch_size(self):
        return self.batch_size

    @property
    def look_back(self):
        return self.look_back

    @property
    def callbacks(self):
        return self.callbacks

    @property
    def datasets_params(self):
        return self.__ml_config.datasets_params

    @property
    def test_set_size(self):
        return self.__ml_config.test_set_size

    @property
    def train_set_size(self):
        return self.__ml_config.train_set_size

    @property
    def sequence_default_length(self):
        return self.__ml_config.datasets_params['sequence_default_length']
