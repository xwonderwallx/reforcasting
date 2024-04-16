#
#
#
#
#
#
#

from enum import Enum


class LogType(Enum):
    Informational = 'Info',
    Warning = 'Warning',
    Error = 'Error',
    Critical = 'Critical',
    Fatal = 'Fatal'