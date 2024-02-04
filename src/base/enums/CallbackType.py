from enum import Enum


class CallbackType(Enum):
    EarlyStopping = 'early_stopping',
    ModelCheckpoint = 'model_checkpoint',
    ReduceLR = 'reduce_lr'