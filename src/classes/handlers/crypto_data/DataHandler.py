# DataHandler.py
# 
#
# Basic operations with data processing
# Base class
#
# 

from abc import ABC, abstractmethod


class DataHandler(ABC):

    @abstractmethod
    def handle(self):
        pass
