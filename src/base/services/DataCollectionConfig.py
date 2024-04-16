from src.base.enums.main.Modules import Modules
from src.base.services.Settings import Settings


class DataCollectionConfig:
    def __init__(self, ml_module_name: Modules):
        self.__ml_module_name = ml_module_name.value
        self.__settings = Settings.get()['data_collection'][self.__ml_module_name]

    @property
    def default_user_agent(self):
        return self.__settings['default_user_agent']

    @property
    def web_scrapping(self):
        return self.__settings['web_scrapping']

    @property
    def html_parser_features(self):
        return self.web_scrapping['html_parser_features']

    @property
    def tag_to_find(self):
        return self.web_scrapping['tag_to_find']

    @property
    def service_name(self):
        return self.web_scrapping['service_name']

    @property
    def version(self):
        return self.web_scrapping['version']
