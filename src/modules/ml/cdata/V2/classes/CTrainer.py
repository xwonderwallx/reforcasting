import pandas as pd

from src.base.classes.BaseTrainer import BaseTrainer
from src.base.enums.TrainingType import TrainingType
from src.base.services.Timer import Timer
from src.modules.ml.cdata.V2.classes.CPreparer import CPreparer


class CTrainer(BaseTrainer):
    def _train_multiple_datasets(self):
        self._timer.start(label='train_multiple_datasets() full time spent')
        for path in self._dataset_paths:
            inner_timer = Timer().start(f"Training on dataset: {path}")
            df = pd.read_csv(path)
            preparer = CPreparer(df)
            prepared_data = preparer.prepare_data()
            sets = prepared_data['sets']
            self._sets = sets
            self._train_one_dataset()  # Train on the current dataset
            inner_timer.stop()
            print(inner_timer.info())
        self._timer.stop()
        print(self._timer.info())

    def _train_one_dataset(self):
        timer = Timer('Training of one dataset').start()
        model = self.model
        compiled_model = self._compile_model(model)
        history = self._fit_model(compiled_model)
        timer.stop()
        print(timer.info())
        return history
