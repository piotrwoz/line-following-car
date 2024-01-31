"""
SettingsReader class is a abstract base class for reading settings from .yaml files.
"""

from abc import ABC
from pathlib import Path
import os

class SettingsReader(ABC):
    """
    Class is abstract base class for derived classes responsible for reading 
    settings from .yaml files.
    """

    def __init__(self):
        self._set_workspace()


    def _set_workspace(self):
        current_workspace = str(Path(__file__).parent)
        os.chdir(current_workspace)
