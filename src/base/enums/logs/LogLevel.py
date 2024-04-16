#
#
#
#
#
#
#

from enum import Enum


class LogLevel(Enum):
    Fatal = "Fatal"
    Blocker = "Blocker"
    Critical = "Critical"
    Medium = "Medium"
    Low = "Low"
    Warning = "Warning"
    Informational = "Informational"
    Debug = "Debug"
    Unknown = "Unknown"

