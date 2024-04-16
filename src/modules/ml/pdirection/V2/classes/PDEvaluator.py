# #
# #
# #
# #
# #
# #
# #
# from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
#
#
# class PDEvaluator:
#     def __init__(self, model, sets):
#         self.__model = model
#         self.__sets = sets
#
#     def evaluate(self):
#         return self.__model.evaluate(self.__sets['x_test_direction'], self.__sets['y_test_direction'])
#
#     # def get_info(self):
#     #     metrics = self.__calculate_evaluation_metrics()
#     #
#     #     # TODO save to logs DB here
#     #     print(f"Evaluation metrics:\n")
#     #     print(f"mse:\t{metrics['mse']}\n")
#     #     print(f"mae:\t{metrics['mae']}\n")
#     #     print(f"r2:\t{metrics['r2']}\n")
#     #
#     # def __calculate_evaluation_metrics(self):
#     #     return {
#     #         'mse': mean_squared_error(self.__real_data, self.__predicted_data),
#     #         'mae': mean_absolute_error(self.__real_data, self.__predicted_data),
#     #         'r2': r2_score(self.__real_data, self.__predicted_data)
#     #     }
