import json
import string


class Config:
    SETTINGS_PATH = './includes/config.json'

    @staticmethod
    def get():
        with open(Config.SETTINGS_PATH, 'r') as settings_json:
            return json.load(settings_json)

    @staticmethod
    def set(key: string, value):
        settings = Config.get()
        settings[key] = value
        with open(Config.SETTINGS_PATH, 'w') as settings_json:
            json.dump(settings, settings_json, indent=4)
