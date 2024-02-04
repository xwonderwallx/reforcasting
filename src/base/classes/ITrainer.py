from abc import ABC, abstractmethod

from keras.src.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau


# TODO change name to DataCollector

class ITrainer(ABC):

    @abstractmethod
    def train(self, ml_module_name):
        self.__ml_module_name = ml_module_name
        pass

    def define_callbacks(self):
        early_stopping = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)
        model_checkpoint = ModelCheckpoint('best_model.keras', save_best_only=True, monitor='val_loss', mode='min')
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.0001)
        return {
            'early_stopping': early_stopping,
            'model_checkpoint': model_checkpoint,
            'reduce_lr': reduce_lr
        }

