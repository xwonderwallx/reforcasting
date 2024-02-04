import pandas as pd
from keras.models import Sequential
from keras.layers import Bidirectional, GRU, Dropout, Dense
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

from src.base.enums.MLModule import MLModule
from src.base.helpers.MLHelper import MLHelper
from src.base.services.Config import Config
from src.modules.ml.cdata.classes.CPreparer import CPreparer  # Adjust the import path as necessary


class CTrainer:
    def __init__(self, dataset_paths):
        self.__sets = None
        self.__settings = Config.get()['ml_model']['cdata']
        self.__dataset_paths = dataset_paths  # List of paths to CSV files
        self.__ml_module = MLModule.CData
        self.__ml_helper = MLHelper(ml_module_name=self.__ml_module)

    def train_multiple_datasets(self):
        for path in self.dataset_paths:
            print(f"Training on dataset: {path}")
            df = pd.read_csv(path)
            preparer = CPreparer(df)
            prepared_data = preparer.prepare_data()
            sets = prepared_data['sets']
            self.__sets = sets
            self.train_one_dataset()  # Train on the current dataset

    def train_one_dataset(self):
        model = self.__define_model()
        compiled_model = self.__compile_model(model)
        history = self.__fit_model(compiled_model)
        # Optional: Evaluate the model using CEvaluator or any custom evaluation method
        # evaluator = CEvaluator(real_data, predicted_data)
        # evaluator.evaluate()
        # evaluator.get_info()

    def __define_model(self):
        features_columns = self.__settings['datasets_params']['features']
        look_back = self.__settings['datasets_params']['look_back']
        # n_features = len(features_columns)
        model = self.__ml_helper.define_model(params=[features_columns, look_back])
        self.__ml_helper.define_model_layers(model=model)
        return model

    def __compile_model(self, model):
        optimizer = self.__ml_helper.define_config_optimizer()
        loss = self.__settings['']
        model.compile(optimizer=optimizer, loss='mean_squared_error')
        return model

    def __define_callbacks(self):
        early_stopping = self.__ml_helper.define_early_stopping()
        model_checkpoint = self.__ml_helper.define_model_checkpoint()
        reduce_lr = self.__ml_helper.define_reduce_lr()
        return [early_stopping, model_checkpoint, reduce_lr]

    def __fit_model(self, model):
        epochs = self.__settings['hyper_parameters']['epochs']
        batch_size = self.__settings['hyper_parameters']['batch_size']
        x_train = self.__sets['x_train']
        y_train = self.__sets['y_train']
        x_test = self.__sets['x_test']
        y_test = self.__sets['y_test']

        callbacks = self.__define_callbacks()

        history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test),
                            callbacks=callbacks)
        return history
