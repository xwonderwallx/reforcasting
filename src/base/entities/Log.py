from datetime import datetime

from src.base.enums.logs.LogLevel import LogLevel
from src.base.services.Config import Config


class Log:
    """
    A class for creating and managing log entries, including message, level, and configuration.

    Attributes:
        __log_message (str): The message to be logged.
        __level (LogLevel): The severity level of the log message, as defined in LogLevel enum.
        __log_config (dict): Configuration settings for logging, obtained from Config.
        __client_url (str): The URL of the client where logs might be sent or stored.
        __log_label (str): A label associated with the log, for categorization or filtering.
        __current_time (datetime): The timestamp when the log entry is created.

    Properties:
        log_message (str): Returns the log message.
        level (LogLevel): Returns the log level.
        log_config (dict): Returns the log configuration settings.
        client_url (str): Returns the client URL from the log configuration.
        log_label (str): Returns the log label from the log configuration.

    Methods:
        to_dict(self) -> dict: Serializes the log entry to a dictionary, suitable for
                               formatting as JSON or storing in a log management system.
    """

    def __init__(self, log_message: str, level: LogLevel = LogLevel.Informational):
        """
        Initializes a new instance of the Log class.

        Parameters:
            log_message (str): The log message to record.
            level (LogLevel, optional): The severity level of the log. Defaults to LogLevel.Informational.
        """
        self.__log_message = log_message
        self.__level = level
        self.__log_config = Config().log
        self.__client_url = self.__log_config['client_url']
        self.__log_label = self.__log_config['log_label']
        self.__current_time = datetime.now()

    @property
    def log_message(self) -> str:
        """Returns the log message."""
        return self.__log_message

    @property
    def level(self) -> LogLevel:
        """Returns the log level."""
        return self.__level

    @property
    def log_config(self) -> dict:
        """Returns the log configuration settings."""
        return self.__log_config

    @property
    def client_url(self) -> str:
        """Returns the client URL from the log configuration."""
        return self.__client_url

    @property
    def log_label(self) -> str:
        """Returns the log label from the log configuration."""
        return self.__log_label

    def to_dict(self) -> dict:
        """
        Serializes the log entry to a dictionary.

        This method is useful for converting the log entry into a format that
        can be easily formatted as JSON, sent to a log management system, or stored
        in a database.

        Returns:
            dict: A dictionary representation of the log entry.
        """
        return {
            "log_config": self.log_config,
            "log_label": self.log_label,
            "log_message": self.log_message,
            "level": self.level.value,
            "current_time": self.__current_time.strftime('%Y-%m-%d %H:%M:%S'),
            "client_url": self.client_url
        }
