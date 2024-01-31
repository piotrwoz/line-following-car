"""
RequestsSettingsReader class is responsible for reading requests settings from .yaml file.
"""

import yaml

from settings_reader import SettingsReader


class RequestsSettingsReader(SettingsReader):
    """
    Class is responsible for reading requests settings from .yaml file necessary for
    successful HTTP communication with robotic car.
    """

    def __init__(self):
        SettingsReader.__init__(self)
        self._path = "../../settings/requests.yaml"
        self._request_timeout = None


    def read(self):
        """Method responsible for reading from .yaml file."""
        try:
            settings = yaml.safe_load(open(file=self._path, mode="r", encoding="utf-8"))
            self._request_timeout = settings['requests-settings']['timeout']
        except FileNotFoundError:
            print(f"Critical error! Can't find {self._path} file with settings!")


    def get_request_timeout(self) -> int:
        """request_timeout getter."""
        return self._request_timeout


if __name__ == "__main__":
    reader = RequestsSettingsReader()
    reader.read()
    print(f"Request timeout [s]: {reader.get_request_timeout()}")
