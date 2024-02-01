"""
PredictedClass enum is storing constants that represents types of available classes to predict
as a result of classification of photos takem by robotic car.
"""

from enum import Enum

class PredictedClass(Enum):
    """
    PredictedClass enum is storing constants that represents types of available classes to predict
    as a result of classification of photos takem by robotic car.
    """

    FORWARD = 0
    BACK = 1
    RIGHT = 2
    LEFT = 3
    SLIGHT_RIGHT = 4
    SLIGHT_LEFT = 5
    THRASH_IMAGE = 6
