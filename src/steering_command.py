"""
SteeringCommand enum is storing constants which represents types of possible steering
commands of robotic car.
"""

from enum import Enum

class SteeringCommand(Enum):
    """
    SteeringCommand enum is storing constants that represents types of available steering commands
    of robotic car.
    """

    START = 0
    STOP = 1
    FORWARD = 2
    BACK = 3
    RIGHT = 4
    LEFT = 5
    CENTER_WHEELS = 6
    SLIGHT_RIGHT = 7
    SLIGHT_LEFT = 8
