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

    STOP = 0
    FORWARD = 1
    BACK = 2
    RIGHT = 3
    SLIGHT_RIGHT = 4
    LEFT = 5
    SLIGHT_LEFT = 6
    CENTER_WHEELS = 7
