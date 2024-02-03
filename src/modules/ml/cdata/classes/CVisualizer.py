#
#
#
#
#
#
#

from src.base.services.Config import Config


class CVisualizer:
    def __init__(self, data):
        self.__data = data
        self.__settings = Config.get()
