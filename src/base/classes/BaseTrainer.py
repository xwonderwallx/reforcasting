from src.base.entities.Dataset import Dataset
from src.base.enums.LogType import LogType
from src.base.enums.main.Modules import Modules
from src.base.enums.exchange.SourceMarket import SourceMarket
from src.base.enums.ml.TrainingType import TrainingType
from src.base.helpers.ExchangeDataHelper import ExchangeDataHelper
from src.base.helpers.LogHelper import LogHelper
from src.base.services.MLConfig import MLConfig
from src.base.services.Timer import Timer


class BaseTrainer:
    """
    A base class for training machine learning models on datasets.

    This class provides an interface for compiling and training models, with the ability to handle
    multiple datasets or a single dataset. It leverages the MLConfig service for model configuration
    and the ExchangeDataHelper to obtain paths for the datasets.

    Attributes:
        _sets: The loaded datasets for training and testing the model.
        _dataset_paths: Paths to CSV files containing trading pair data.
        _timer: A Timer instance for tracking operation durations.
        _ml_helper: An MLConfig instance for obtaining model configuration.
        __settings: The settings obtained from the current MLConfig instance.

    Methods:
        __init__(self, ml_module_name=Modules.CData): Initializes the trainer with a machine learning module name.
        model (property): Defines and returns a machine learning model based on the MLConfig.
        train(self, training_type: TrainingType): Trains the model based on the specified training type.
        _train_multiple_datasets(self): Placeholder for training on multiple datasets.
        _train_one_dataset(self): Placeholder for training on a single dataset.
        _define_model(self): Obtains the configured model from MLConfig.
        _compile_model(self, model): Compiles the model with an optimizer and loss function.
        _fit_model(self, model): Fits the model to the training data.
        _split_to_sets(self): Splits the dataset into training and testing sets.

    Usage:
        To train a model on a single dataset:
        >>> trainer = BaseTrainer(ml_module_name=Modules.CData)
        >>> trainer.train(TrainingType.One)

        To train a model on multiple datasets:
        >>> trainer.train(TrainingType.Multiple)
    """

    def __init__(self, ml_module_name: Modules = Modules.CData):
        # TODO set another sourceMarkets to the config file
        try:
            self._dataset_paths = ExchangeDataHelper.paths_to_trading_pairs_exchange_data(
                source_market=SourceMarket.Binance)  # List of paths to CSV files
            self._timer = Timer()
            self._ml_helper = MLConfig(ml_module_name=ml_module_name)
            self.__settings = self._ml_helper.current_module_settings
            self.__path = None
            self.__preparer = None
        except Exception as e:
            LogHelper.pretty_print(e,
                                   f'{LogHelper.default_log_label()} | The parameters passed into constructor are not '
                                   f'valid')

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        self.__path = value

    @property
    def model(self):
        return self._define_model()

    @property
    def preparer(self):
        return self.__preparer

    @preparer.setter
    def preparer(self, value):
        self.__preparer = value

    @property
    def sets(self):
        try:
            return self.preparer['sets']
        except Exception as e:
            print(f"Exception during extracting datasets: {e.args}")

    def train(self, training_type: TrainingType):
        if training_type == TrainingType.One:
            return self._train_one_dataset()
        if training_type == TrainingType.Multiple:
            return self._train_multiple_datasets()
        return None

    def _train_multiple_datasets(self):
        return False

    def _train_one_dataset(self):
        return False

    def _define_model(self):
        return self._ml_helper.configured_model

    def _compile_model(self, model):
        optimizer = self._ml_helper.configured_optimizer
        loss = self._ml_helper.compiling_loss
        model.compile(optimizer=optimizer, loss=loss)
        return model

    def _fit_model(self, model):
        try:
            x_test, x_train, y_test, y_train = self._split_to_sets()
            callbacks = self._ml_helper.callbacks
            return model.fit(x_train, y_train, epochs=self._ml_helper.epochs, batch_size=self._ml_helper.batch_size,
                             validation_data=(x_test, y_test),
                             callbacks=callbacks)
        except Exception as e:
            LogHelper.pretty_print(e.with_traceback(None), f"Fitting model failed, exception was:", LogType.Error.value)
            return False

    def _split_to_sets(self):
        return self.sets.x_test, self.sets.x_train, self.sets.y_test, self.sets.y_train
