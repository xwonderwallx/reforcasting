from src.base.services.Settings import Settings


class Config:
    def __init__(self):
        self.__config = Settings.get()['configuration']
        self.__paths = self.__config['paths']
        self.__exchange_data = self.__config['exchange_data']
        self.__google_keys = self.__config['google']['keys']

    @property
    def exchange_data_path(self):
        return self.__paths['exchange_data']

    @property
    def models_path(self):
        return self.__paths['models']

    @property
    def gs_api_key(self):
        return self.__google_keys['google_search_api_key']

    @property
    def gs_engine_key(self):
        return self.__google_keys['google_search_engine_id']
