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


class Logger(Singleton):

    def __init__(self, sender_email='', recipient_email='', smtp_server='', password='', initial_text='', debug_label='', log_label=''):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.text = []
            if initial_text == '':
                self.text.append(initial_text)

            self.sender_email = sender_email if sender_email != '' else LogHelper.SENDER_EMAIL
            self.recipient_email = recipient_email if recipient_email != '' else LogHelper.RECIPIENT_EMAIL
            self.smtp_server = smtp_server if smtp_server != '' else LogHelper.SMTP_SERVER
            self.password = password if password != '' else LogHelper.PASSWORD

            self.debug_label = debug_label if debug_label != '' else LogHelper.DEBUG_LABEL
            self.subject = LogHelper.LOG_LABEL if log_label != '' else LogHelper.LOG_LABEL

    def add_log(self, log):
        self.text.append(f"{self.debug_label} | {log}")

    def send_logs_email(self):
        array_str = pprint.pformat(self.text)

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = self.subject
        msg.attach(MIMEText(array_str, 'plain'))

        server = smtplib.SMTP(self.smtp_server, 587)
        server.starttls()
        server.login(self.sender_email, self.password)
        server.send_message(msg)
        server.quit()

    def __del__(self):
        self.send_logs_email()
