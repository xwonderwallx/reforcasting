from abc import ABC, abstractmethod

from src.base.entities.Dataset import Dataset
from src.base.enums.Modules import Modules
from src.base.enums.SourceMarket import SourceMarket
from src.base.helpers.ExchangeDataHelper import ExchangeDataHelper
from src.base.services.MLConfig import MLConfig
from src.base.services.Timer import Timer


class BaseTrainer(ABC):

    def __init__(self):
        self.__sets = None
        self.__ml_helper = MLConfig(ml_module_name=Modules.CData)
        self.__settings = self.__ml_helper.current_module_settings
        self.__dataset_paths = ExchangeDataHelper.paths_to_trading_pairs_exchange_data(source_market=SourceMarket.Binance)  # List of paths to CSV files
        self.__timer = Timer()

    @property
    def model(self):
        return self._define_model()

    @abstractmethod
    def train_multiple_datasets(self):
        pass

    @abstractmethod
    def train_one_dataset(self):
        pass

    @abstractmethod
    def train(self, ml_module_name):
        pass

    def _define_model(self):
        return self.__ml_helper.configured_model()

    def _compile_model(self, model):
        optimizer = self.__ml_helper.configured_optimizer
        loss = self.__ml_helper.compiling_loss
        model.compile(optimizer=optimizer, loss=loss)
        return model

    def _fit_model(self, model):
        epochs = self.__ml_helper.epochs
        batch_size = self.__ml_helper.batch_size
        dataset = Dataset(self.__sets)

        x_train = dataset.x_train
        y_train = dataset.y_train
        x_test = dataset.x_test
        y_test = dataset.y_test

        callbacks = MLConfig.callbacks

        history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test),
                            callbacks=callbacks)
        return history

