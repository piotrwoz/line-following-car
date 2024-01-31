"""
In this source file there NameDateType enum which defines type of name to generate.
"""

from enum import Enum

class DateNameType(Enum):
    """
    NameDateType enum represents types of available file names formats
    of robotic car.
    """
    DATE_HOUR_MINUTE_SECONDS = 0
    DATE_HOUR_MINUTE = 1
