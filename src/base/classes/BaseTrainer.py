from src.base.entities.Dataset import Dataset
from src.base.enums.Modules import Modules
from src.base.enums.SourceMarket import SourceMarket
from src.base.enums.TrainingType import TrainingType
from src.base.helpers.ExchangeDataHelper import ExchangeDataHelper
from src.base.services.MLConfig import MLConfig
from src.base.services.Timer import Timer


class BaseTrainer:

    def __init__(self, ml_module_name=Modules.CData):
        self._sets = None
        self._dataset_paths = ExchangeDataHelper.paths_to_trading_pairs_exchange_data(
            source_market=SourceMarket.Binance)  # List of paths to CSV files
        self._timer = Timer()
        self._ml_helper = MLConfig(ml_module_name=ml_module_name)
        self.__settings = self._ml_helper.current_module_settings

    @property
    def model(self):
        return self._define_model()

    def train(self, training_type: TrainingType):
        match training_type:
            case TrainingType.One:
                return self._train_one_dataset()
            case TrainingType.Multiple:
                return self._train_multiple_datasets()
            case _:
                return None

    def _train_multiple_datasets(self):
        pass

    def _train_one_dataset(self):
        pass

    def _define_model(self):
        return self._ml_helper.configured_model()

    def _compile_model(self, model):
        optimizer = self._ml_helper.configured_optimizer
        loss = self._ml_helper.compiling_loss
        model.compile(optimizer=optimizer, loss=loss)
        return model

    def _fit_model(self, model):
        epochs = self._ml_helper.epochs
        batch_size = self._ml_helper.batch_size
        x_test, x_train, y_test, y_train = self._split_to_sets()
        callbacks = MLConfig.callbacks
        return model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test),
                         callbacks=callbacks)

    def _split_to_sets(self):
        dataset = Dataset(self._sets)
        x_train = dataset.x_train
        y_train = dataset.y_train
        x_test = dataset.x_test
        y_test = dataset.y_test
        return x_test, x_train, y_test, y_train
