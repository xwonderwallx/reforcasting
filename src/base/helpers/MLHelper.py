from keras.src.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.src.layers import Bidirectional, Dropout, GRU, Dense
from keras.src.models.cloning import Sequential
from keras.src.optimizers.adam import Adam

from src.base.enums.CallbackType import CallbackType
from src.base.enums.MLModule import MLModule
from src.base.enums.ModelLayer import ModelLayer
from src.base.enums.ModelType import ModelType
from src.base.enums.OptimizerType import OptimizerType
from src.base.services.Config import Config


class MLHelper:

    def __init__(self, ml_module_name: MLModule):
        self.__ml_module_name = ml_module_name
        self.__settings = Config.get()['ml_model'][f'{ml_module_name}']
        self.__callbacks_settings = self.__settings['hyper_parameters']['callbacks']
        self.__layers = self.__settings['hyper_parameters']['model_layers']
        self.__model_type = self.__settings['hyper_parameters']['model_type']

    @property
    def look_back(self):
        return self.hyper_parameters['look_back']

    @property
    def batch_size(self):
        return self.hyper_parameters['batch_size']

    @property
    def model_type(self):
        return self.__model_type

    @property
    def epochs(self):
        return self.hyper_parameters['epochs']

    @property
    def features(self):
        return self.hyper_parameters['features']

    @property
    def callbacks(self):
        return self.__get_configured_callbacks()

    @property
    def callbacks_types(self):
        return self.__callbacks_settings.keys()

    @property
    def hyper_parameters(self):
        return self.__settings['hyper_parameters']

    @property
    def configured_model(self):
        model = self.__define_model()
        model = self.__define_model_layers(model)
        return model

    def __get_configured_callbacks(self):
        configured_callbacks = []
        for callback in self.__callbacks_settings.keys():
            if callback == CallbackType.EarlyStopping:
                configured_callbacks.append({CallbackType.EarlyStopping: self.define_early_stopping()})
            if callback == CallbackType.ModelCheckpoint:
                configured_callbacks.append({CallbackType.ModelCheckpoint: self.define_model_checkpoint()})
            if callback == CallbackType.ReduceLR:
                configured_callbacks.append({CallbackType.ReduceLR: self.define_reduce_lr()})
        return configured_callbacks

    def define_early_stopping(self):
        monitor = self.__callbacks_settings['early_stopping']['monitor']
        patience = self.__callbacks_settings['early_stopping']['patience']
        restore_best_weights = self.__callbacks_settings['early_stopping']['restore_best_weights']
        return EarlyStopping(monitor=monitor, patience=patience, restore_best_weights=restore_best_weights)

    def define_model_checkpoint(self):
        filepath = self.__settings['model_checkpoint']['save_file_path']
        save_best_weights = self.__settings['model_checkpoint']['save_best_only']
        monitor = self.__callbacks_settings['model_checkpoint']['monitor']
        mode = self.__callbacks_settings['model_checkpoint']['mode']
        return ModelCheckpoint(filepath=filepath, save_best_only=save_best_weights, monitor=monitor, mode=mode)

    def define_reduce_lr(self):
        monitor = self.__callbacks_settings['reduce_lr']['monitor']
        factor = self.__callbacks_settings['reduce_lr']['factor']
        patience = self.__callbacks_settings['reduce_lr']['patience']
        min_lr = self.__callbacks_settings['reduce_lr']['min_lr']
        return ReduceLROnPlateau(monitor=monitor, factor=factor, patience=patience, min_lr=min_lr)

    def define_config_optimizer(self):
        optimizer = self.__callbacks_settings['compiling']['optimizer']
        if optimizer['name'] == OptimizerType.Adam:
            return self.__define_adam_optimizer()

    def __define_model(self, params=None):
        if self.__model_type == ModelType.Sequential:
            return Sequential(params)
        raise Exception(f"Unknown model type: {self.__model_type}")

    def __define_model_layers(self, model=None):
        layers = self.__layers.keys()
        for layer in layers:
            model = self.__add_layer(layer=layer, model=model)
        return model

    def __define_adam_optimizer(self):
        learning_rate = self.__callbacks_settings['compiling']['compiling']['learning_rate']
        return Adam(learning_rate=learning_rate)

    def __define_layer(self, level, params=None):
        current_layer = self.__layers[level]
        layer_name = current_layer['name']
        if layer_name == ModelLayer.Bidirectional:
            return self.__define_bidirectional_layer(layer_settings=current_layer[layer_name], input_shape=params)
        if layer_name == ModelLayer.Dropout:
            return self.__dropout_layer(layer_settings=current_layer[layer_name])
        if layer_name == ModelLayer.Dense:
            return self.__dense_layer(layer_settings=current_layer[layer_name])

    def __define_bidirectional_layer(self, layer_settings, input_shape=None):
        params = self.__bidirectional_layer_params(settings=layer_settings, input_shape=input_shape)
        return Bidirectional(params)

    def __bidirectional_layer_params(self, settings, input_shape=None):
        if settings['key_name'] == ModelLayer.GRU:
            return self.__define_gru(settings, input_shape)

    def __define_gru(self, settings, input_shape=None):
        units = settings['gru']['units']
        return_sequences = settings['gru']['return_sequences']
        if input_shape is not None:
            return GRU(units=units, return_sequences=return_sequences, input_shape=input_shape)
        else:
            return GRU(units=units, return_sequences=return_sequences)

    def __dropout_layer(self, layer_settings):
        dropout_rate = layer_settings['dropout']
        return Dropout(dropout_rate)

    def __dense_layer(self, layer_settings):
        dense = layer_settings['dense']
        return Dense(dense)

    def __add_layer(self, layer, model, params=None):
        model.add(self.__define_layer(level=layer, params=params))
        return model
