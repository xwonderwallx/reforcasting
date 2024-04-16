from src.base.classes.BaseVisualizer import BaseVisualizer
from src.base.services.Settings import Settings


class Visualizer(BaseVisualizer):
    def __init__(self, data):
        super().__init__(data)
        self.__settings = Settings.get()
