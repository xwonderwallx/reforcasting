#
#
#
#
#
#
#


import json
import string


class Settings(object):
    SETTINGS_PATH = './includes/settings.json'

    @staticmethod
    def get():
        with open(Settings.SETTINGS_PATH, 'r') as settings_json:
            return json.load(settings_json)

    @staticmethod
    def set(key: string, value):
        settings = Settings.get()
        settings[key] = value
        with open(Settings.SETTINGS_PATH, 'w') as settings_json:
            json.dump(settings, settings_json, indent=4)
