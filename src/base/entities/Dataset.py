from src.base.enums.SetType import SetType


class Dataset:

    def __init__(self, separated_sets: dict):
        self.__sets = separated_sets
        self.__keys = separated_sets.keys()
        if self.__check_permissions() is False:
            raise Exception("The dataset is incorrectly formatted.")


    @property
    def x_train(self):
        return self.__sets[SetType.XTrain]

    @property
    def y_train(self):
        return self.__sets[SetType.YTrain]

    @property
    def x_test(self):
        return self.__sets[SetType.XTest]

    @property
    def y_test(self):
        return self.__sets[SetType.YTest]

    def __check_permissions(self):
        if SetType.YTest not in self.__sets:
            return False
        if SetType.XTrain not in self.__sets:
            return False
        if SetType.YTest not in self.__sets:
            return False
        if SetType.YTrain not in self.__sets:
            return False
        return True
