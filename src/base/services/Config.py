#
#
#
#
#

import configparser
from src.base.services.Logger import Logger


class Config:
    CONFIG_PATH = './includes/config.ini'

    def __init__(self):
        section = 'google'
        self.__search_api_key = self.__config().get(section, 'google_search_api_key')
        self.__search_engine_id = self.__config().get(section, 'google_search_engine_id')

    def __config(self):
        config_path = Config.CONFIG_PATH
        config = configparser.ConfigParser()
        config.read(config_path)

        Logger().add_log(f"{Config.CONFIG_PATH} | Config is initialized")
        print("Sections found: ", config.sections())

        return config

    def get_search_engine_id(self):
        return self.__search_engine_id

    def get_search_api_key(self):
        return self.__search_api_key
