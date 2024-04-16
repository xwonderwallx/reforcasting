import json
import string


class Settings:
    """
    A utility class for managing application settings stored in a JSON file.

    This class provides static methods to read from and write to a JSON-based
    settings file. It is designed to facilitate easy access and modification
    of configuration settings throughout the application.

    Attributes:
        SETTINGS_PATH (str): The filesystem path to the JSON file containing the settings.

    Methods:
        get(): Reads and returns the settings from the JSON file.
        set(key: str, value): Updates a specific setting in the JSON file.
    """

    SETTINGS_PATH = './includes/config.json'

    @staticmethod
    def get():
        """
        Reads and returns the settings from the JSON file.

        This method opens the JSON settings file in read-only mode, parses it,
        and returns the content as a dictionary.

        Returns:
            dict: The settings contained in the JSON file.
        """
        with open(Settings.SETTINGS_PATH, 'r') as settings_json:
            return json.load(settings_json)

    @staticmethod
    def set(key: string, value):
        """
        Updates a specific setting in the JSON file.

        This method reads the current settings, updates the value for the given
        key, and writes the modified settings back to the JSON file. If the key
        does not exist, it will be added to the settings.

        Parameters:
            key (str): The key in the settings to update.
            value: The new value to set for the given key.

        Note:
             The `value` parameter's type depends on the specific setting being updated.
             It could be a string, a number, an array, or another dictionary.
        """
        settings = Settings.get()
        settings[key] = value
        with open(Settings.SETTINGS_PATH, 'w') as settings_json:
            json.dump(settings, settings_json, indent=4)
