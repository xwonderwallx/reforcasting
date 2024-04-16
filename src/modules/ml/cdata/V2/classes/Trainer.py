import pandas as pd

from src.base.classes.BaseTrainer import BaseTrainer
from src.base.enums.main.Modules import Modules
from src.base.helpers.LogHelper import LogHelper
from src.base.services.Timer import Timer
from src.modules.ml.cdata.V2.classes.Preparer import Preparer


class Trainer(BaseTrainer):
    """
    A class responsible for training machine learning models on financial datasets.

    This class handles the training of models on multiple datasets, as well as individual training sessions. It uses
    a timer to keep track of the duration of training processes and employs a Preparer to preprocess datasets before training.

    Methods:
        _train_multiple_datasets(self): Trains models on multiple datasets.
        _train_one_dataset(self): Trains a model on a single dataset.

    Usage:
        The class is used internally within the machine learning system and assumes access to multiple dataset paths
        and a model provided by the BaseTrainer. To train on multiple datasets, call _train_multiple_datasets().
        To train on a single dataset, call _train_one_dataset() with a dataset already set in self._sets.
    """

    def __init__(self, ml_module_name: Modules = Modules.CData):
        super().__init__(ml_module_name)
        self._path = None

    @property
    def path(self):
        return self.path

    @path.setter
    def path(self, value):
        self._path = value

    def _train_multiple_datasets(self):
        """
        Trains models on multiple datasets.

        Iterates over dataset paths provided in self._dataset_paths, reads each dataset, preprocesses it using the Preparer class,
        and then trains a model using the _train_one_dataset method. Training duration for each dataset is timed and printed.
        """
        print(f'CData.Trainer._train_multiple_datasets()')
        try:
            # self._timer.start(label='train_multiple_datasets() full time spent')
            for path in self._dataset_paths:
                inner_timer = Timer().start(f"Training on dataset: {path}")
                self.path = path
                print(f"PATH: {path}")

                df = pd.read_csv(path)
                LogHelper.pretty_print(df, 'The data frame has been read')

                self.preparer = Preparer(df=df, ml_module_name=Modules.CData).prepare()
                LogHelper.pretty_print(self.preparer, 'The data frame has been prepared')

                LogHelper.pretty_print(self.preparer['sets'], f'{LogHelper.default_log_label()} | sets')
                self.__sets = Preparer(df, Modules.CData).prepare()['sets']
                self._train_one_dataset()  # Train on the current dataset
                # inner_timer.stop()
                # print(inner_timer.info())
            # self._timer.stop()
            # print(self._timer.info())
            return True
        except Exception as e:
            print(f"Exception during training multiple datasets: {e.args}")
            return False

    def _train_one_dataset(self):
        """
        Trains a model on a single dataset.

        Trains a model on the dataset currently set in self._sets. The dataset is assumed to be preprocessed and ready for training.
        The method compiles the model, fits it to the dataset, and times the training process.

        Returns:
            The training history object containing information about the training session.
        """
        print('CData.Trainer._train_one_dataset()')
        try:
            timer = Timer('Training of one dataset')
            timer.start()
            model = self._define_model()
            compiled_model = self._compile_model(model)
            history = self._fit_model(compiled_model)
            timer.stop()
            print(timer.info())
            return history, True
        except Exception as e:
            print(f'An exception occurred during training of one dataset: {str(e)}')
            return False
