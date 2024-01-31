"""
NetworkSettingsReader class is responsible for reading network settings from .yaml file.
"""

import yaml

from settings_reader import SettingsReader


class NetworkSettingsReader(SettingsReader):
    """
    Class is responsible for reading network settings from .yaml file necessary for
    robotic car to connect to Wi-Fi network.
    """

    def __init__(self):
        SettingsReader.__init__(self)
        self._path = "../../settings/network.yaml"
        self._network_name = None
        self._ipv4 = None
        self._password = None


    def read(self):
        """Method responsible for reading from .yaml file."""
        try:
            settings = yaml.safe_load(open(file=self._path, mode="r", encoding="utf-8"))
            self._network_name = settings['wifi-settings']['network-name']
            self._ipv4 = settings['wifi-settings']['ipv4']
            self._password = str(settings['wifi-settings']['password'])
        except FileNotFoundError:
            print(f"Critical error! Can't find {self._path} file with settings!")


    def get_network_name(self) -> str:
        """network_name getter."""
        return self._network_name


    def get_ipv4(self) -> str:
        """ipv4 getter."""
        return self._ipv4


    def get_password(self) -> str:
        """password getter."""
        return self._password


if __name__ == "__main__":
    reader = NetworkSettingsReader()
    reader.read()
    print(f"Network name: {reader.get_network_name()}")
    print(f"IPv4: {reader.get_ipv4()}")
    print(f"Password: {reader.get_password()}")
