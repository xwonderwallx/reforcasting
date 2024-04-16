import inspect
import json
import os
from pprint import pprint

from src.base.enums.LogType import LogType


class LogHelper:
    @staticmethod
    def pretty_print(data, label, log_type: LogType = None):
        log_type = log_type.value if log_type is not None else LogType.Informational.value
        try:
            print(f'[{log_type}] | {label}: {json.dumps(data, indent=4)}\n')
        except Exception as e:
            pprint(f'[{log_type}] | {label}: {data}\n')

    @staticmethod
    def get_current_function_name():
        return inspect.currentframe().f_code.co_name

    @staticmethod
    def default_log_label():
        log_params = LogHelper.log_params()
        return f'{log_params["dir"]}.{log_params["func"]}'

    @staticmethod
    def current_directory():
        return os.getcwd()

    @staticmethod
    def log_params():
        return {
            'dir': LogHelper.current_directory(),
            'func': LogHelper.get_current_function_name()
        }
