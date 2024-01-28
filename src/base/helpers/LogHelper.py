#
# src.helpers.LogHelper.py
#
#
#
#
#
import inspect


class LogHelper:
    SENDER_EMAIL = 'vika010501@gmail.com'
    RECIPIENT_EMAIL = 'vika010501@gmail.com'
    SMTP_SERVER = 'smtp.gmail.com'
    PASSWORD = 'Heli5copter@@1'

    LOG_LABEL = '[Log][Alpha][reforcast_model]'
    DEBUG_LABEL = f'{inspect.currentframe().f_code.co_name}'