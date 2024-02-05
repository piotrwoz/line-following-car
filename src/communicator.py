"""
Communicator class is responsible for communication between computer and robotic car.
"""

import os
import shutil
import time
import requests

from settings_readers.network_settings_reader import NetworkSettingsReader
from settings_readers.requests_settings_reader import RequestsSettingsReader
from settings_readers.drive_settings_reader import DriveSettingsReader
from steering_command import SteeringCommand
from date_to_str import DateToStr, DateNameType


class Communicator:
    """
    Class is responsible for communication between computer and robotic car.
    It is done via HTTP requests.
    """

    def __init__(self):
        self._import_from_network_settings()
        self._import_from_drive_settings()
        self._import_from_requests_settings()
        self._set_url_bases()

        self._last_command = None
        self._is_wheels_centered = True
        self._is_driving_forward = False
        self._is_driving_backward = False

        self._offset = 8
        self._turn_sleep_s = 0.15

        self._path_to_dataset = "../../dataset/"


    def _import_from_network_settings(self):
        network_settings_reader = NetworkSettingsReader()
        network_settings_reader.read()
        self._ipv4 = network_settings_reader.get_ipv4()


    def _import_from_drive_settings(self):
        drive_settings_reader = DriveSettingsReader()
        drive_settings_reader.read()
        self._max_forward = drive_settings_reader.get_max_forward()
        self._standard_forward = drive_settings_reader.get_standard_forward()
        self._max_backward = drive_settings_reader.get_max_backward()
        self._standard_backward = drive_settings_reader.get_standard_backward()
        self._stop = drive_settings_reader.get_stop()
        self._max_turn_right = drive_settings_reader.get_max_turn_right()
        self._slight_turn_right = drive_settings_reader.get_slight_turn_right()
        self._max_turn_left = drive_settings_reader.get_max_turn_left()
        self._slight_turn_left = drive_settings_reader.get_slight_turn_left()
        self._center = drive_settings_reader.get_center()


    def _import_from_requests_settings(self):
        requests_settings_reader = RequestsSettingsReader()
        requests_settings_reader.read()
        self._request_timeout = requests_settings_reader.get_request_timeout()


    def _set_url_bases(self):
        self._url = f"http://{self._ipv4}"
        self._drive_url = f"{self._url}/drive?speed="
        self._turn_url = f"{self._url}/drive?turn="
        self._photo_url = f"{self._url}/photo"


    def send_request(self, command: SteeringCommand):
        """
        Interface of possible steering commands that change robotic car movement.
        """
        self._last_command = command
        match command:
            case SteeringCommand.START:
                self.start_drive()
            case SteeringCommand.STOP:
                self.stop_drive()
            case SteeringCommand.FORWARD:
                self.forward_drive()
            case SteeringCommand.BACK:
                self.back_drive()
            case SteeringCommand.RIGHT:
                self.turn(command)
            case SteeringCommand.SLIGHT_RIGHT:
                self.turn(command)
            case SteeringCommand.LEFT:
                self.turn(command)
            case SteeringCommand.SLIGHT_LEFT:
                self.turn(command)
            case SteeringCommand.CENTER_WHEELS:
                self.center_wheels()
            case _:
                print("Unknown request type")


    def start_drive(self):
        """Handle starting robotic car drive: start driving straight and set proper flags."""
        self.center_wheels()
        self.drive(self._standard_forward)
        self._is_driving_forward = True
        self._is_driving_backward = False


    def stop_drive(self):
        """Handle stopping robotic car drive: start driving straight and set proper flags."""
        self.stop()
        self.center_wheels()
        self._is_driving_forward = False
        self._is_driving_backward = False


    def forward_drive(self):
        """Handle forward drive: start driving straight and set proper flags."""
        if not self._is_wheels_centered:
            self.center_wheels()
        if not self._is_driving_forward:
            self.drive(self._standard_forward)
            self._is_driving_forward = True
            self._is_driving_backward = False


    def back_drive(self):
        """Handle back drive: start driving back and set proper flags."""
        self.drive(self._standard_backward)
        if not self._is_driving_backward:
            self.drive(self._standard_backward)
            self._is_driving_forward = False
            self._is_driving_backward = True


    def drive(self, speed_parameter: int):
        """
        Method responsible for sending GET request with speed parameter for 
        driving forward or backward.
        """
        if speed_parameter < self._max_forward and speed_parameter > self._max_backward:
            url_to_send = f"{self._drive_url}{speed_parameter}"
            self._send_get_request(url_to_send, speed_parameter)


    def stop(self):
        """
        Method responsible for sending GET request for stop the robotic car.
        """
        url_to_send = f"{self._drive_url}{self._stop}"
        self._send_get_request(url_to_send, self._stop)


    def turn(self, command: SteeringCommand):
        """
        Method responsible for sending GET request with turn type parameter.
        """
        self._is_wheels_centered = False
        turn_parameter = self._map_turn_car_command(command)
        turn_parameter = self._turn_parameter_mapper(turn_parameter)
        url_to_send = f"{self._turn_url}{turn_parameter}"
        time.sleep(self._turn_sleep_s)
        self._send_get_request(url_to_send, turn_parameter)


    def _map_turn_car_command(self, command: SteeringCommand):
        turn_parameter = None
        match command:
            case SteeringCommand.RIGHT:
                turn_parameter = self._max_turn_right
            case SteeringCommand.SLIGHT_RIGHT:
                turn_parameter = self._slight_turn_right
            case SteeringCommand.LEFT:
                turn_parameter = self._max_turn_left
            case SteeringCommand.SLIGHT_LEFT:
                turn_parameter = self._slight_turn_left
            case _:
                turn_parameter = 0

        return turn_parameter


    def center_wheels(self):
        """
        Method responsible for sending GET request for straighten the robotic car wheels.
        """
        self._is_wheels_centered = True
        turn_parameter = self._turn_parameter_mapper(self._center)
        url_to_send = f"{self._turn_url}{turn_parameter}"
        self._send_get_request(url_to_send, turn_parameter)


    def _turn_parameter_mapper(self, turn_parameter: int) -> int:
        """
        Due to fabric settings there is an offset in turn parameter. In this model
        turn_parameter = 8 straightens the wheels.
        Method returns input parameter corrected by offset.
        """
        turn_parameter += self._offset
        return turn_parameter


    def _send_get_request(self, url_to_send: str, parameter: int):
        try:
            requests.get(url = url_to_send, params = parameter, timeout = self._request_timeout)
        except requests.Timeout:
            print(f"TIMEOUT when sending {url_to_send} request")


    def take_photo(self) -> requests.models.Response:
        """
        Method responsible for taking a picture with robotic car's camera.
        Method returns .jpg file stored in bytes.
        """
        try:
            response = requests.get(
                url=self._photo_url,
                timeout=self._request_timeout,
                stream=True
            )
            return response
        except requests.Timeout:
            print("TIMEOUT during taking picture!")

        return None


    def take_photo_and_save(self, subdirectory_to_store: str = ""):
        """
        Method responsible for taking a picture with robotic car's camera and saving it on a disk.
        Use for creating own dataset.
        """
        response = self.take_photo()
        if response is not None:
            self._save_photo_on_disc(response, subdirectory_to_store)
        else:
            print("Didn't receive a photo from robotic car!")


    def _save_photo_on_disc(self, response: requests.Response, subdirectory_to_store: str):
        name_based_on_date = DateToStr.parse_date(DateNameType.DATE_HOUR_MINUTE_SECONDS)
        filename = f"img_{name_based_on_date}.jpg"
        subdirectory_to_store = self._fix_separator_in_subdirectory(subdirectory_to_store)
        directory_path =  f"{self._path_to_dataset}{subdirectory_to_store}"
        self._create_dataset_directory(directory_path)
        path = f"{directory_path}{filename}"
        if response.status_code == 200:
            with open(file=path, mode='wb') as file:
                shutil.copyfileobj(response.raw, file)
                print(f'Sucessfully taken photo: {filename}')


    def _fix_separator_in_subdirectory(self, subdirectory: str) -> str:
        if subdirectory[-1] != "/":
            subdirectory = subdirectory + "/"

        return subdirectory


    def _create_dataset_directory(self, directory: str):
        if not os.path.exists(directory):
            os.makedirs(directory)


    def get_last_command(self) -> SteeringCommand:
        """Last steering command getter."""
        return self._last_command


if __name__ == "__main__":
    communicator = Communicator()
    for _ in range(0, 20):
        communicator.take_photo_and_save("../dataset/train/thrash")
        time.sleep(1)
