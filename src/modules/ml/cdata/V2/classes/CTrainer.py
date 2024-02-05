import pandas as pd

from src.base.classes.BaseTrainer import BaseTrainer
from src.base.services.Timer import Timer
from src.modules.ml.cdata.classes.CPreparer import CPreparer


class CTrainer(BaseTrainer):
    def __init__(self):
        super().__init__()

    def train(self, data):
        pass

    def train_multiple_datasets(self):
        self.__timer.start(label='train_multiple_datasets() full time spent')
        for path in self.__dataset_paths:
            inner_timer = Timer().start(f"Training on dataset: {path}")
            df = pd.read_csv(path)
            preparer = CPreparer(df)
            prepared_data = preparer.prepare_data()
            sets = prepared_data['sets']
            self.__sets = sets
            self.train_one_dataset()  # Train on the current dataset
            inner_timer.stop()
            print(inner_timer.info())
        self.__timer.stop()
        print(self.__timer.info())

    def train_one_dataset(self):
        timer = Timer('Training of one dataset').start()
        model = self.model
        compiled_model = self._compile_model(model)
        history = self._fit_model(compiled_model)
        timer.stop()
        print(timer.info())
        return history
