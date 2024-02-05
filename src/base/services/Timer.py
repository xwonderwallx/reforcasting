import time


class Timer:
    def __init__(self, label=''):
        self.__start_time = None
        self.__stop_time = None
        self.__label = label

    def start(self, label=''):
        self.__start_time = time.time()
        if label is not '':
            self.__label = label

    def stop(self):
        self.__stop_time = time.time()

    def info(self):
        if self.__start_time is None or self.__stop_time is None:
            return f"{self.__label} | Timer is not set or stopped yet."
        else:
            return f"{self.__label} | Time passed: {self.__stop_time - self.__start_time}."

    def refresh_timer(self):
        self.__start_time = None
        self.__stop_time = None
