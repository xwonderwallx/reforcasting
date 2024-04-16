from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.src.layers import Bidirectional, Dropout, GRU, Dense
from keras.src.optimizers.adam import Adam
from keras.models import Sequential

from src.base.enums.main.Modules import Modules
from src.base.enums.ml.CallbackType import CallbackType
from src.base.enums.ml.InputShape import InputShape
from src.base.enums.ml.ModelLayer import ModelLayer
from src.base.enums.ml.ModelType import ModelType
from src.base.enums.ml.OptimizerType import OptimizerType
from src.base.helpers.LogHelper import LogHelper
from src.base.services.Settings import Settings


class MLConfig:
    """
    A configuration class for setting up machine learning models, including defining
    the model architecture, compiling settings, and specifying callbacks.

    This class provides an interface to configure various aspects of a machine learning model
    based on settings defined in a JSON configuration file. It supports configuring model
    types, layers, optimization parameters, and training callbacks.

    Attributes:
        __ml_module_name (Modules): The machine learning module name as defined in the Enums.
        __settings (dict): Loaded settings from the JSON file for the specified ML module.
        __callbacks_settings (dict): Specific settings related to callbacks within the ML configuration.
        __layers (dict): Configuration for the model layers as specified in the ML settings.
        __model_type (str): The type of model to be created, e.g., Sequential.
        __datasets_params (dict): Parameters related to dataset splitting and preparation.

    Properties:
        current_module_settings: Retrieves the current module settings from the configuration.
        look_back: The look-back period for the model.
        batch_size: Batch size for the model training.
        model_type: The type of the model being configured.
        epochs: The number of epochs for model training.
        features: The features to be used in the model.
        callbacks: Configured callback instances for the model training.
        callbacks_types: The types of callbacks as defined in the settings.
        compiling_loss: The loss function to be used for compiling the model.
        datasets_params: Parameters related to dataset management.
        test_set_size: The size ratio of the test dataset.
        train_set_size: The size ratio of the training dataset.
        hyper_parameters: Hyperparameters for the model training and architecture.
        tech_indicators: Technical indicators used as features in the model.
        configured_model: The fully configured model ready for training.
        configured_optimizer: The optimizer configured for the model.

    Methods:
        __init__(self, ml_module_name: Modules): Initializes the MLConfig object with the specified ML module name.
        __define_model(self, params=None): Defines the model based on the specified type.
        __define_model_layers(self, model=None): Adds the configured layers to the model.
        __define_early_stopping(self): Configures the early stopping callback.
        __define_model_checkpoint(self): Configures the model checkpoint callback.
        __define_reduce_lr(self): Configures the reduce learning rate callback.
        __get_configured_callbacks(self): Returns instances of configured callbacks.
        __define_adam_optimizer(self): Defines the Adam optimizer with specified parameters.
        __define_layer(self, level, params=None): Defines a specific layer based on the configuration.
        __define_bidirectional_layer(self, layer_settings): Defines a bidirectional layer.
        __define_gru(self, settings): Defines a GRU layer with specified settings.
        __add_layer(self, layer, model, params=None): Adds a defined layer to the model.
        __get_input_shape(self, settings): Determines the input shape for the model based on settings.
        __define_input_shape(self, input_shape_settings: InputShape): Defines the input shape for the model.
    """

    def __init__(self, ml_module_name: Modules):
        """
        Initializes the MLConfig object with settings specific to the provided machine learning module name.

        Parameters:
            ml_module_name (Modules): An enumeration value representing the machine learning module.
        """
        self.__ml_module_name = ml_module_name.value
        self.__settings = Settings.get()['ml_model'][self.__ml_module_name]
        self.__callbacks_settings = self.__settings['hyper_parameters']['callbacks']
        self.__layers = self.__settings['hyper_parameters']['model_layers']
        self.__model_type = self.__settings['hyper_parameters']['model_type']
        self.__datasets_params = self.__settings['datasets_params']
        self.__compiling = self.__settings['hyper_parameters']['compiling']

    @property
    def current_module_settings(self):
        """Retrieves the current module settings from the configuration."""
        return Settings.get()['ml_model'][self.__ml_module_name]

    @property
    def look_back(self):
        """The look-back period for the model."""
        return self.hyper_parameters['look_back']

    @property
    def batch_size(self):
        """Batch size for the model training."""
        return self.hyper_parameters['batch_size']

    @property
    def model_type(self):
        """The type of the model being configured."""
        return self.__model_type

    @property
    def epochs(self):
        """The number of epochs for model training."""
        return self.hyper_parameters['epochs']

    @property
    def features(self):
        """The features to be used in the model."""
        return self.hyper_parameters['features']

    @property
    def callbacks(self):
        """Configured callback instances for the model training."""
        return self.__get_configured_callbacks()

    @property
    def callbacks_types(self):
        """The types of callbacks as defined in the settings."""
        return self.__callbacks_settings.keys()

    @property
    def compiling_loss(self):
        """The loss function to be used for compiling the model."""
        return self.hyper_parameters['compiling']['loss']

    @property
    def datasets_params(self):
        """Parameters related to dataset management."""
        return self.__datasets_params

    @property
    def test_set_size(self):
        """The size ratio of the test dataset."""
        return self.datasets_params['test_set']['size']

    @property
    def train_set_size(self):
        """The size ratio of the training dataset."""
        return self.datasets_params['train_set']['size']

    @property
    def hyper_parameters(self):
        """Hyperparameters for the model training and architecture."""
        return self.__settings['hyper_parameters']

    @property
    def tech_indicators(self):
        """Technical indicators used as features in the model."""
        return self.__settings['technical_indicators']

    @property
    def configured_model(self):
        """The fully configured model ready for training."""
        model = self.__define_model()
        print(model)
        model = self.__define_model_layers(model)
        return model

    @property
    def configured_optimizer(self):
        """The optimizer configured for the model."""
        optimizer = self.__compiling['optimizer']
        LogHelper.pretty_print(optimizer, 'configured_optimizer')

        if optimizer['name'] == OptimizerType.Adam.value:
            return self.__define_adam_optimizer()
        return None

    @staticmethod
    def __dropout_layer(layer_settings):
        dropout_rate = layer_settings
        print("Dropout rate: ", dropout_rate)
        return Dropout(layer_settings)

    @staticmethod
    def __dense_layer(layer_settings):
        dense = layer_settings['units']
        return Dense(dense)

    @staticmethod
    def __get_input_shape_settings(settings):
        if 'input_shape' in settings.keys():
            return settings['input_shape']
        return None

    def __define_early_stopping(self):
        monitor = self.__callbacks_settings['early_stopping']['monitor']
        patience = self.__callbacks_settings['early_stopping']['patience']
        restore_best_weights = self.__callbacks_settings['early_stopping']['restore_best_weights']
        return EarlyStopping(monitor=monitor, patience=patience, restore_best_weights=restore_best_weights)

    def __define_model_checkpoint(self):
        filepath = self.__callbacks_settings['model_checkpoint']['save_file_path']
        save_best_weights = self.__callbacks_settings['model_checkpoint']['save_best_only']
        monitor = self.__callbacks_settings['model_checkpoint']['monitor']
        mode = self.__callbacks_settings['model_checkpoint']['mode']
        model_checkpoint = ModelCheckpoint(filepath=filepath, save_best_only=save_best_weights, monitor=monitor,
                                           mode=mode)
        return model_checkpoint

    def __define_reduce_lr(self):
        monitor = self.__callbacks_settings['reduce_lr']['monitor']
        factor = self.__callbacks_settings['reduce_lr']['factor']
        patience = self.__callbacks_settings['reduce_lr']['patience']
        min_lr = self.__callbacks_settings['reduce_lr']['min_lr']
        return ReduceLROnPlateau(monitor=monitor, factor=factor, patience=patience, min_lr=min_lr)

    def __get_configured_callbacks(self):
        configured_callbacks = []

        for callback in self.callbacks_types:
            if callback == CallbackType.EarlyStopping.value:
                configured_callbacks.append({CallbackType.EarlyStopping.value: self.__define_early_stopping()})
            elif callback == CallbackType.ModelCheckpoint.value:
                configured_callbacks.append({CallbackType.ModelCheckpoint.value: self.__define_model_checkpoint()})
            elif callback == CallbackType.ReduceLR.value:
                configured_callbacks.append({CallbackType.ReduceLR.value: self.__define_reduce_lr()})

        return configured_callbacks

    def __define_model(self, params=None):
        print(self.__model_type)
        if self.__model_type == ModelType.Sequential.value:
            return Sequential()
        raise Exception(f"Unknown model type: {self.__model_type}")

    def __define_model_layers(self, model=None):
        layers = self.__layers.keys()
        print(f"Configured model layers: {layers}")
        for layer in layers:
            print(f"layer: {layer}")
            model = self.__add_layer(layer=layer, model=model)
            print(f"model: {model}")
        return model

    def __define_adam_optimizer(self):
        learning_rate = self.__compiling['optimizer']['learning_rate']
        return Adam(learning_rate=learning_rate)

    def __define_layer(self, level, params=None):
        current_layer = self.__layers[level]
        layer_name = current_layer['name']
        layer_settings = current_layer.get(layer_name, {})

        if layer_name == ModelLayer.Bidirectional.value:
            return self.__define_bidirectional_layer(layer_settings=layer_settings)
        if layer_name == ModelLayer.Dropout.value:
            return MLConfig.__dropout_layer(layer_settings=layer_settings)
        if layer_name == ModelLayer.Dense.value:
            return MLConfig.__dense_layer(layer_settings=layer_settings)

    def __define_bidirectional_layer(self, layer_settings):
        params = self.__bidirectional_layer_params(settings=layer_settings)
        return Bidirectional(params)

    def __bidirectional_layer_params(self, settings):
        if settings['key_name'] == ModelLayer.GRU.value:
            return self.__define_gru(settings)

    def __define_gru(self, settings):
        gru = settings['gru']
        units = gru['units']
        return_sequences = gru['return_sequences']
        input_shape = self.__get_input_shape(settings=settings)

        if input_shape is not None:
            return GRU(units=units, return_sequences=return_sequences, input_shape=input_shape)
        else:
            return GRU(units=units, return_sequences=return_sequences)

    def __add_layer(self, layer, model, params=None):
        defined_layer = self.__define_layer(level=layer, params=params)
        if defined_layer is not None:
            model.add(defined_layer)
        else:
            raise Exception("Unexpected layer")
        return model

    def __get_input_shape(self, settings):
        input_shape_settings = MLConfig.__get_input_shape_settings(settings=settings)
        if input_shape_settings is not None:
            return self.__define_input_shape(input_shape_settings=input_shape_settings)
        return None

    def __define_input_shape(self, input_shape_settings: InputShape):
        input_shape = []
        for setting in input_shape_settings.value:
            if setting == InputShape.LookBack.value:
                input_shape.append(self.look_back)
            if setting == InputShape.NFeatures.value:
                input_shape.append(len(self.features))
        if len(input_shape) != 0:
            return input_shape
        return None
