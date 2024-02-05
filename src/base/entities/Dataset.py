class Dataset:

    def __init__(self, separated_sets):
        self.__sets = separated_sets

    @property
    def x_train(self):
        return self.__sets['x_train']

    @property
    def y_train(self):
        return self.__sets['y_train']

    @property
    def x_test(self):
        return self.__sets['x_test']

    @property
    def y_test(self):
        return self.__sets['y_test']
