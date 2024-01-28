#
#
#
#
#
#
#

import numpy as np
import pandas as pd
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import GRU, Dropout, Dense
from keras.models import Sequential
from keras.optimizers import Adam
from keras.src.callbacks import ReduceLROnPlateau
from keras.src.layers import Bidirectional
from sklearn.preprocessing import MinMaxScaler

from src.base.services.Settings import Settings
from src.modules.cdata.classes.CPreparer import CPreparer


class CTrainer:
    def __init__(self, sets):
        self.__settings = Settings.get()
        self.__sets = sets

    def train(self):
        # df = pd.DataFrame(self.__prepared_data)
        # params = {
        #     'features_columns': features_columns
        # }
        model = self.__define_model()
        compiled_model = self.__compile_model(model)
        return self.__fit_model(model)


    # def __get_training_and_testing_sets(self):
    #     training_data_len = int(len(df_scaled) * 0.8)
    #     return X[:training_data_len], X[training_data_len:], Y[:training_data_len], Y[training_data_len:]


    def __define_model(self):
        features_columns = self.__settings['ml_model']['cdata']['datasets_params']['features']
        look_back = self.__settings['ml_model']['cdata']['datasets_params']['look_back']
        n_features = len(features_columns)

        model = Sequential()
        model.add(Bidirectional(GRU(128, return_sequences=True, input_shape=(look_back, n_features))))
        model.add(Dropout(0.4))
        model.add(Bidirectional(GRU(64, return_sequences=False)))
        model.add(Dropout(0.4))
        model.add(Dense(1))

        return model

    def __compile_model(self, model):
        adam = Adam(learning_rate=0.0005)
        model.compile(optimizer=adam, loss='mean_squared_error')
        return model

    def __define_callbacks(self):
        early_stopping = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)
        model_checkpoint = ModelCheckpoint('best_model.keras', save_best_only=True, monitor='val_loss', mode='min')
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.0001)
        return {
            'early_stopping': early_stopping,
            'model_checkpoint': model_checkpoint,
            'reduce_lr': reduce_lr
        }

    def __fit_model(self, model):
        epochs = self.__settings['ml_model']['cdata']['hyper_parameters']['epochs']
        batch_size = self.__settings['ml_model']['cdata']['hyper_parameters']['batch_size']

        x_train = self.__sets['x_train']
        y_train = self.__sets['y_train']
        x_test = self.__sets['x_test']
        y_test = self.__sets['y_test']

        callbacks = self.__define_callbacks()

        return model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test),
                         callbacks=[callbacks['early_stopping'], callbacks['model_checkpoint'], callbacks['reduce_lr']])
