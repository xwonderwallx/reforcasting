#
# src/classes/MoodState.py
#
# MoodState enum used to give a characteristic grade about cryptocurrency news
#


from enum import Enum


class MoodState(Enum):
    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1
