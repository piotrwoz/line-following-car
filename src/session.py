"""
Main app session.
"""

import sys
import threading

from commandline_args_parser import CommandLineArgsParser
from ai_model.model_handler import ModelHandler
from communicator import Communicator
from steering_command import SteeringCommand
from timer import Timer
from music_player import MusicPlayer


class Session:
    """
    Class is responsible for main app session. It calls training model,
    creates object responsible for communication with robotic car and 
    steers robotic car.
    """

    def __init__(self):
        self._command_line_args_parser = CommandLineArgsParser()
        self._command_line_args_parser.print_args()

        self._model_handler = None
        try:
            self._model_handler = ModelHandler(self._command_line_args_parser)
        except FileNotFoundError:
            print("Fail when loading model file. Shutting down!")
            sys.exit(-1)

        self._communicator = Communicator()
        self._exit_flag = threading.Event()


    def start_session(self):
        """
        Starting robotic car session
        """
        mode = self._command_line_args_parser.get_mode()
        match mode:
            case "train":
                self._model_training()
            case "run":
                self._start_car()
            case _:
                print("Unknown mode. Shutting down!")


    def _model_training(self):
        self._model_handler.train_model()


    def _start_car(self):
        main_thread = threading.Thread(target=self._main_loop)

        timer = Timer(self._command_line_args_parser.get_time(), self._exit_flag)
        timer_thread = threading.Thread(target=timer.start_timer)

        if self._check_if_play_music():
            self._run_music_player_thread()
        main_thread.start()
        timer_thread.start()

        main_thread.join()
        print("Program has finished.")


    def _main_loop(self):
        print("Starting main loop of application")
        while not self._exit_flag.is_set():
            # response = self._communicator.take_photo()
            # if response is not None:
            #     predicted_label = self._model_handler.classify_image(response)
            #     print(f"Predicted command: {predicted_label}")
            #     self._send_command_based_on_label(predicted_label)
            # else:
            #     print("No response")
            pass

        # self._turn_off_car()


    def _send_command_based_on_label(self, label: str):
        match label:
            case "forward":
                self._communicator.send_request(SteeringCommand.FORWARD)
            case "back":
                self._communicator.send_request(SteeringCommand.BACK)
            case "right":
                self._communicator.send_request(SteeringCommand.RIGHT)
            case "slightly_right":
                self._communicator.send_request(SteeringCommand.SLIGHT_RIGHT)
            case "left":
                self._communicator.send_request(SteeringCommand.LEFT)
            case "slightly_left":
                self._communicator.send_request(SteeringCommand.SLIGHT_LEFT)
            case _:
                print("Unknown label predicted. Turning off robotic car.")
                self._turn_off_car()


    def _turn_off_car(self):
        self._communicator.send_request(SteeringCommand.STOP)
        self._communicator.send_request(SteeringCommand.CENTER_WHEELS)


    def _check_if_play_music(self):
        if (self._command_line_args_parser.get_music() is True and
            self._command_line_args_parser.get_mode() in ('run')):
            return True

        return False


    def _run_music_player_thread(self):
        music_player = MusicPlayer(self._exit_flag)
        music_thread = threading.Thread(target=music_player.play_music)
        music_thread.start()
        music_thread.join()
