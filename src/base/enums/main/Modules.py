#
# src/classes/MoodState.py
#
# MoodState enum used to give a characteristic grade about cryptocurrency news
#


from enum import Enum


class Modules(Enum):
    CData = 'cdata'
    PDirection = 'pdirection'
    CNews = 'cnews'
