from src.base.services.Settings import Settings


class Config:
    """
    A configuration handler class for accessing various configuration settings.

    This class provides a centralized interface to access configuration settings
    loaded from a JSON file via the `Settings` service. It abstracts away the details
    of accessing individual configuration sections, such as paths, exchange data,
    Google API keys, and logging configurations.

    Attributes:
        __config (dict): A dictionary holding the entire configuration loaded from the JSON file.
        __paths (dict): A subset of __config that contains filesystem paths configurations.
        __exchange_data (dict): A subset of __config specific to exchange data configurations.
        __google_keys (dict): A subset of __config that contains Google API keys.

    Properties:
        trading_pairs: Returns a dictionary of trading pairs configured for exchange data.
        exchange_data_path: Returns the filesystem path for storing exchange data.
        models_path: Returns the filesystem path for storing models.
        gs_api_key: Returns the Google Search API key.
        gs_engine_key: Returns the Google Search Engine ID.
        log: Returns logging configurations.

    Methods:
        __init__(self): Initializes the Config object by loading configuration settings
                           from the `Settings` service and parsing relevant subsections.
    """

    def __init__(self):
        """
        Initializes the Config object by loading the configuration from the `Settings` service.
        The configuration is expected to be a dictionary with nested dictionaries for various settings.
        """
        self.__config = Settings.get()['configuration']
        self.__paths = self.__config['paths']
        self.__exchange_data = self.__config['exchange_data']
        self.__google_keys = self.__config['google']['keys']

    @property
    def trading_pairs(self):
        """Returns a dictionary of trading pairs for exchange data."""
        return self.__exchange_data['trading_pairs']

    @property
    def exchange_data_path(self):
        """Returns the filesystem path for storing exchange data."""
        return self.__paths['exchange_data']

    @property
    def models_path(self):
        """Returns the filesystem path for storing models."""
        return self.__paths['models']

    @property
    def gs_api_key(self):
        """Returns the Google Search API key."""
        return self.__google_keys['google_search_api_key']

    @property
    def gs_engine_key(self):
        """Returns the Google Search Engine ID."""
        return self.__google_keys['google_search_engine_id']

    @property
    def log(self):
        """Returns logging configurations."""
        return self.__config['log']
