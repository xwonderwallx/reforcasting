#
#
#
#
#
#
#

from enum import Enum


class ModelLayer(Enum):
    Bidirectional = 'bidirectional',
    GRU = 'gru',
    Dropout = 'dropout',
    Dense = 'dense'
