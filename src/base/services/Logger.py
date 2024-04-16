# src.services.Logger.py
#
# Own logger class is made to make logs
# Use add_log(log) to add logs in the final output
# __del__() writes log to the list and sends it to email
#
# PLEASE USE get_instance() method to implement Singleton pattern
#

import json
import atexit
import requests

from src.base.entities.Log import Log
from src.base.entities.Singleton import Singleton
from src.base.services.Config import Config


class Logger(Singleton):

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self.__config = Config().log
            self.__client_url = self.__config['client_url']
            self.__log_label = self.__config['log_label']
            self.__logs = []
            self._initialized = True
            atexit.register(self.cleanup)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    @staticmethod
    def get_instance():
        # Ensure Singleton pattern enforcement
        if not hasattr(Logger, "_instance"):
            Logger._instance = Logger()
        return Logger._instance

    def add_log(self, log: Log):
        self.__logs.append(log)

    def cleanup(self):
        self.send_logs_to_client()

    def send_logs_to_client(self):
        logs_data = [log.to_dict() for log in self.__logs]
        payload = {
            self.__log_label: logs_data
        }
        headers = {'Content-Type': 'application/json'}

        # Send the logs as a JSON payload to the client URL
        try:
            response = requests.post(self.__client_url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()  # Raises an exception for 4XX/5XX errors
            print(f"Logs successfully sent to client: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send logs to client: {e}")
