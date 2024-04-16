import time


class Timer:
    """
    A simple timer class for measuring elapsed time between events.

    This class offers a straightforward way to start, stop, and report the
    elapsed time for operations or code blocks. It's useful for performance
    measurements, debugging, or simply timing operations.

    Attributes:
        __start_time (float): The start time of the timer. None if the timer hasn't started.
        __stop_time (float): The stop time of the timer. None if the timer hasn't stopped.
        __label (str): An optional label to identify the timer instance.

    Methods:
        __init__(self, label=''): Constructs a Timer instance with an optional label.
        start(self, label=''): Starts or restarts the timer with an optional new label.
        stop(self): Stops the timer.
        info(self): Returns a string with the label and elapsed time.
        refresh_timer(self): Resets the start and stop times to None, allowing the timer to be reused.
    """

    def __init__(self, label=''):
        """
        Initializes a new Timer instance.

        Parameters:
            label (str, optional): An optional label to identify the timer. Defaults to an empty string.
        """
        self.__start_time = None
        self.__stop_time = None
        self.__label = label

    def start(self, label=''):
        """
        Starts or restarts the timer, recording the current time as the start time.

        If a label is provided, it updates the timer's label. If the timer is already
        running, it will reset the start time to the current time.

        Parameters:
            label (str, optional): An optional new label for the timer. Defaults to an empty string.
        """
        self.__start_time = time.time()
        if label:
            self.__label = label

    def stop(self):
        """
        Stops the timer, recording the current time as the stop time.

        This method records the current time as the stop time, effectively stopping the timer.
        The elapsed time can then be retrieved with the `info` method.
        """
        self.__stop_time = time.time()

    def info(self):
        """
        Returns a string containing the timer's label and the elapsed time.

        If the timer has not been started or stopped, it returns a message indicating that
        the timer is not set or stopped yet. Otherwise, it returns the elapsed time.

        Returns:
            str: A string with the timer's label and the elapsed time, or a message indicating
                 that the timer is not properly set.
        """
        if self.__start_time is None or self.__stop_time is None:
            return f"{self.__label} | Timer is not set or stopped yet."
        else:
            elapsed_time = self.__stop_time - self.__start_time
            return f"{self.__label} | Time passed: {elapsed_time} seconds."

    def refresh_timer(self):
        """
        Resets the timer's start and stop times.

        This method allows the timer to be reused by setting both the start and stop times
        back to None. After calling this method, the timer must be started again to measure a new duration.
        """
        self.__start_time = None
        self.__stop_time = None
