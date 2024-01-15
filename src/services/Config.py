#
#
#
#
#

import configparser
from src.services.Logger import Logger


class Config:
    CONFIG_PATH = './includes/config.ini'

    def __init__(self):
        section = 'google'
        self.search_api_key = self.config().get(section, 'google_search_api_key')
        self.search_engine_id = self.config().get(section, 'google_search_engine_id')

    def config(self):
        config_path = Config.CONFIG_PATH
        config = configparser.ConfigParser()
        config.read(config_path)

        Logger().add_log(f"{Config.CONFIG_PATH} | Config is initialized")
        print("Sections found: ", config.sections())

        return config

    def get_search_engine_id(self):
        return self.search_engine_id

    def get_search_api_key(self):
        return self.search_api_key
