# #
# # src.services.CryptocurrencyDataPreparer.py
# #
# #
# #
# #
# #
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import MinMaxScaler
#
# from src.base.classes.IPreparer import IPreparer
#
#
# class PDPreparer(IPreparer):
#     def __init__(self, df):
#         super().__init__()
#         self.__df = df
#
#     def prepare_data(self):
#         scaler = MinMaxScaler(feature_range=(0, 1))
#         scaled_data = scaler.fit_transform(self.__df)
#         df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
#         time_steps = 60
#         X, y = self.create_dataset(scaled_data, df['Target'].values, time_steps)
#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
#         weights = class_weight.compute_class_weight('balanced', np.unique(y_train), y_train)
#         class_weights = {i: weights[i] for i in range(2)}
#
#
#
#     def create_dataset(X, y, time_steps=1):
#         Xs, ys = [], []
#         for i in range(len(X) - time_steps):
#             Xs.append(X[i:(i + time_steps)])
#             ys.append(y[i + time_steps])
#         return np.array(Xs), np.array(ys)
#
