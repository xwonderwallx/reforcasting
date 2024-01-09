# Logger.py
#
# Own logger class is made to make logs
# Use add_log(log) to add logs in the final output
# __del__() writes log to the .. and sends it to email


class Logger:
    def __init__(self, initial_text = ''):
        self.text = []
        self.text.append(initial_text)

    def add_log(self, log):
        pass

    def __del__(self):
        pass