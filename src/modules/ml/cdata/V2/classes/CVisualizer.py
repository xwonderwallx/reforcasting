#
#
#
#
#
#
#

from src.base.services.Settings import Settings


class CVisualizer:
    def __init__(self, data):
        self.__data = data
        self.__settings = Settings.get()
