#
#
#
#
#
#
#

from keras.layers import GRU, Dropout, Dense
from keras.models import Sequential
from keras.src.layers import Bidirectional

from src.base.enums.main.Modules import Modules
from src.base.services.MLConfig import MLConfig


class CTrainer:
    def __init__(self, sets):
        self.__ml_helper = MLConfig(Modules.CData)
        self.__settings = self.__ml_helper.current_module_settings
        self.__sets = sets

    def train(self):
        # df = pd.DataFrame(self.__prepared_data)
        # params = {
        #     'features_columns': features_columns
        # }
        model = self.__define_model()
        compiled_model = self.__compile_model(model)
        history = self.__fit_model(compiled_model)
        return {
            'history': history,
            'model': model
        }

    # def __get_training_and_testing_sets(self):
    #     training_data_len = int(len(df_scaled) * 0.8)
    #     return X[:training_data_len], X[training_data_len:], Y[:training_data_len], Y[training_data_len:]

    def __define_model(self):
        features_columns = self.__settings['datasets_params']['features']
        look_back = self.__settings['datasets_params']['look_back']
        n_features = len(features_columns)

        model = Sequential()
        model.add(Bidirectional(GRU(128, return_sequences=True, input_shape=(look_back, n_features))))
        model.add(Dropout(0.4))
        model.add(Bidirectional(GRU(64, return_sequences=False)))
        model.add(Dropout(0.4))
        model.add(Dense(1))

        return model

    def __compile_model(self, model):
        adam = self.__ml_helper.configured_optimizer()
        loss = self.__settings['hyper_parameters']['compiling']['loss']
        model.compile(optimizer=adam, loss=loss)
        return model

    def __define_callbacks(self):
        return {
            'early_stopping': self.__ml_helper.__define_early_stopping(),
            'model_checkpoint': self.__ml_helper.__define_model_checkpoint(),
            'reduce_lr': self.__ml_helper.__define_reduce_lr()
        }

    def __fit_model(self, model):
        epochs = self.__settings['hyper_parameters']['epochs']
        batch_size = self.__settings['hyper_parameters']['batch_size']
        print(self.__sets.keys())
        x_train = self.__sets['x_train']
        y_train = self.__sets['y_train']
        x_test = self.__sets['x_test']
        y_test = self.__sets['y_test']

        callbacks = self.__define_callbacks()

        return model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test),
                         callbacks=[callbacks['early_stopping'], callbacks['model_checkpoint'], callbacks['reduce_lr']])
