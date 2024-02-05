"""
NetworkSettingsReader class is responsible for reading drive parameters settings from .yaml file.
"""

import yaml

from settings_readers.settings_reader import SettingsReader


class DriveSettingsReader(SettingsReader):
    """
    Class is responsible for reading drive parameters settings from .yaml file.
    """

    def __init__(self):
        SettingsReader.__init__(self)
        self._path = "../../settings/drive.yaml"
        self._max_forward = None
        self._standard_forward = None
        self._max_backward = None
        self._standard_backward = None
        self._stop = None
        self._max_turn_right = None
        self._slight_turn_right = None
        self._max_turn_left = None
        self._slight_turn_left = None
        self._center = None


    def read(self):
        """Method responsible for reading from .yaml file."""
        try:
            settings = yaml.safe_load(open(file=self._path, mode="r", encoding="utf-8"))
            self._max_forward = settings['drive-parameters-ranges']['drive']['max-forward']
            self._standard_forward = settings['drive-parameters-ranges']['drive']['standard-forward']
            self._max_backward = settings['drive-parameters-ranges']['drive']['max-backward']
            self._standard_backward = settings['drive-parameters-ranges']['drive']['standard-backward']
            self._stop = settings['drive-parameters-ranges']['drive']['stop']
            self._max_turn_right = settings['drive-parameters-ranges']['turn']['max-right']
            self._slight_turn_right = settings['drive-parameters-ranges']['turn']['slight-right']
            self._max_turn_left = settings['drive-parameters-ranges']['turn']['max-left']
            self._slight_turn_left = settings['drive-parameters-ranges']['turn']['slight-left']
            self._center = settings['drive-parameters-ranges']['turn']['center']
        except FileNotFoundError:
            print(f"Critical error! Can't find {self._path} file with settings!")


    def get_max_forward(self) -> int:
        """max_forward getter."""
        return self._max_forward


    def get_standard_forward(self) -> int:
        """standard_forward getter."""
        return self._standard_forward


    def get_max_backward(self) -> int:
        """max_forward getter."""
        return self._max_backward


    def get_standard_backward(self) -> int:
        """standard_backward getter."""
        return self._standard_backward


    def get_stop(self) -> int:
        """stop getter."""
        return self._stop


    def get_max_turn_right(self) -> int:
        """max_turn_right getter."""
        return self._max_turn_right


    def get_max_turn_left(self) -> int:
        """max_turn_left getter."""
        return self._max_turn_left


    def get_slight_turn_right(self) -> int:
        """slight_turn_right getter."""
        return self._slight_turn_right


    def get_slight_turn_left(self) -> int:
        """slight_turn_left getter."""
        return self._slight_turn_left


    def get_center(self) -> int:
        """center getter."""
        return self._center


if __name__ == "__main__":
    reader = DriveSettingsReader()
    reader.read()
    print(f"Max forward: {reader.get_max_forward()}")
    print(f"Standard forward: {reader.get_standard_forward()}")
    print(f"Max backward: {reader.get_max_backward()}")
    print(f"Standard backward: {reader.get_standard_backward()}")
    print(f"Stop: {reader.get_stop()}")
    print(f"Max turn right: {reader.get_max_turn_right()}")
    print(f"Slight turn right: {reader.get_slight_turn_right()}")
    print(f"Max turn left: {reader.get_max_turn_left()}")
    print(f"Slight turn left: {reader.get_slight_turn_left()}")
    print(f"Center: {reader.get_center()}")
