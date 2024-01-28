# DataHandler.py
# 
#
# Basic operations with data processing
# Base class
#
# 

from abc import ABC, abstractmethod


# TODO change name to DataCollector

class IHandler(ABC):

    @abstractmethod
    def handle(self):
        pass
