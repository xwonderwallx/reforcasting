# #
# #
# #
# #
# #
# #
# #
#
# from keras.callbacks import EarlyStopping
# from keras.layers import GRU, Dropout, Dense
# from keras.models import Sequential
# from keras.optimizers import Adam
# from keras.src.callbacks import ReduceLROnPlateau, ModelCheckpoint
# from keras.src.layers import Bidirectional
#
# from src.base.services.Settings import Settings
#
#
# class PDTrainer:
#     def __init__(self, sets):
#         self.__settings = Settings.get()
#         self.__sets = sets
#         self.__hyper_params = self.__settings['ml_model']['pdirection']['hyper_parameters']
#         self.__layers = self.__hyper_params['model_layers']
#         self.__callbacks = self.__hyper_params['callbacks']
#
#     def train(self):
#         # df = pd.DataFrame(self.__prepared_data)
#         # params = {
#         #     'features_columns': features_columns
#         # }
#         model = self.__define_model()
#         compiled_model = self.__compile_model(model)
#         history = self.__fit_model(compiled_model)
#         return {
#             'history': history,
#             'model': model
#         }
#
#     # def __get_training_and_testing_sets(self):
#     #     training_data_len = int(len(df_scaled) * 0.8)
#     #     return X[:training_data_len], X[training_data_len:], Y[:training_data_len], Y[training_data_len:]
#
#     def __add_model_layers(self, layers_params, look_back, n_features):
#         direction_model = Sequential()
#         direction_model.add(Bidirectional(GRU(
#             units=layers_params['first']['units'],
#             return_sequences=layers_params['first']['return_sequences'],
#             input_shape=(look_back, n_features))))
#         direction_model.add(Dropout(layers_params['second']['dropout']))
#         direction_model.add(Bidirectional(GRU(
#             units=layers_params['third']['units'],
#             return_sequences=layers_params['third']['return_sequences'])))
#         direction_model.add(Dropout(layers_params['fourth']['dropout']))
#         direction_model.add(Dense(
#             units=layers_params['fifth']['units'],
#             activation=layers_params['fifth']['activation_function']))
#         return direction_model
#
#     def __compile_model(self, model):
#         model.compile(
#             optimizer=self.__get_adam_optimizer(),
#             loss=self.__hyper_params['compiling']['optimizer']['loss'],
#             metrics=self.__hyper_params['compiling']['optimizer']['metrics'])
#         return model
#
#     def __define_model(self):
#         # look_back = self.__hyper_params['look_back']
#         # n_features = len(self.__hyper_params['features'])
#         # layers_params = self.__get_layers_params()
#         # direction_model = self.__add_model_layers(layers_params, look_back, n_features)
#         #
#         # return direction_model
#
#         model = Sequential()
#         model.add(Bidirectional(GRU(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2]))))
#         model.add(Dropout(0.2))
#         model.add(Bidirectional(GRU(50)))
#         model.add(Dropout(0.2))
#         model.add(Dense(1, activation='sigmoid'))
#
#         model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
#
#         # Обучение модели
#         callbacks = [EarlyStopping(monitor='val_loss', patience=10),
#                      ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.00001)]
#
#         history = model.fit(X_train, y_train, epochs=100, batch_size=32,
#                             validation_data=(X_test, y_test),
#                             class_weight=class_weights, callbacks=callbacks)
#
#     def __define_callbacks(self):
#         early_stopping = self.__get_early_stopping()
#         model_checkpoint = self.__get_model_checkpoint()
#         reduce_lr = self.__get_reduce_lr()
#         return {
#             'early_stopping': early_stopping,
#             'model_checkpoint': model_checkpoint,
#             'reduce_lr': reduce_lr
#         }
#
#     def __get_adam_optimizer(self):
#         print(f"Optimizer: {self.__hyper_params['compiling']['optimizer']['name']}")
#         return Adam(learning_rate=self.__hyper_params['compiling']['optimizer']['learning_rate'])
#
#     def __get_reduce_lr(self):
#         return ReduceLROnPlateau(
#             monitor=self.__callbacks['reduce_lr']['monitor'],
#             factor=self.__callbacks['reduce_lr']['factor'],
#             patience=self.__callbacks['reduce_lr']['patience'],
#             min_lr=self.__callbacks['reduce_lr']['min_lr'])
#
#     def __get_model_checkpoint(self):
#         return ModelCheckpoint(
#             filepath=self.__callbacks['model_checkpoint']['save_file_path'],
#             save_best_only=self.__callbacks['model_checkpoint']['save_best_only'],
#             monitor=self.__callbacks['model_checkpoint']['monitor'],
#             mode=self.__callbacks['model_checkpoint']['mode'])
#
#     def __get_early_stopping(self):
#         return EarlyStopping(
#             monitor=self.__callbacks['early_stopping']['monitor'],
#             patience=self.__callbacks['early_stopping']['patience'],
#             restore_best_weights=self.__callbacks['early_stopping']['restore_best_weights'])
#
#     def __fit_model(self, model):
#         epochs = self.__hyper_params['epochs']
#         batch_size = self.__hyper_params['batch_size']
#
#         x_train = self.__sets['x_train']
#         y_train = self.__sets['y_train']
#         x_test = self.__sets['x_test']
#         y_test = self.__sets['y_test']
#
#         callbacks = self.__define_callbacks()
#
#         return model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test),
#                          callbacks=callbacks)
#
#     def __get_layers_params(self):
#         return {
#             'first': {
#                 'units': self.__layers['first']['bidirectional']['gru']['units'],
#                 'return_sequences': self.__layers['first']['bidirectional']['gru']['return_sequences']
#             },
#             'second': {
#                 'dropout': self.__layers['second']['dropout']
#             },
#             'third': {
#                 'units': self.__layers['third']['bidirectional']['gru']['units'],
#                 'return_sequences': self.__layers['third']['bidirectional']['gru']['return_sequences']
#             },
#             'fourth': {
#                 'dropout': self.__layers['fourth']['dropout']
#             },
#             'fifth': {
#                 'units': self.__layers['fifth']['dense']['units'],
#                 'activation_function': self.__layers['fifth']['dense']['activation_function']
#             }
#         }