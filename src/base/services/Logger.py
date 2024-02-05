# src.services.Logger.py
#
# Own logger class is made to make logs
# Use add_log(log) to add logs in the final output
# __del__() writes log to the list and sends it to email
#
#
import pprint
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.base.entities.Singleton import Singleton
from src.base.helpers.LogHelper import LogHelper
from src.base.services.Settings import Settings


class Logger(Singleton):

    @property
    def logger(self):
        return self.__logs

    def __init__(self):
        # if not hasattr(self, 'initialized'):
        #     self.initialized = True
        #     self.text = []
        #     if initial_text == '':
        #         self.text.append(initial_text)
        #
        #     self.sender_email = sender_email if sender_email != '' else LogHelper.SENDER_EMAIL
        #     self.recipient_email = recipient_email if recipient_email != '' else LogHelper.RECIPIENT_EMAIL
        #     self.smtp_server = smtp_server if smtp_server != '' else LogHelper.SMTP_SERVER
        #     self.password = password if password != '' else LogHelper.PASSWORD
        #
        #     self.debug_label = debug_label if debug_label != '' else LogHelper.DEBUG_LABEL
        #     self.subject = LogHelper.LOG_LABEL if log_label != '' else LogHelper.LOG_LABEL

        self.__settings = Settings.get()['logger']
        self.__client_url = self.__settings['client_url']
        self.__log_label = self.__settings['log_label']
        self.__logs = []

    def add_log(self, log):
        self.__logs.append(f"{self.__log_label} | {log}")

    def send_logs_to_client(self):
        pass
