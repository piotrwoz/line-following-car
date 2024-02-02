"""
Main app session.
"""

import sys
import threading

from commandline_args_parser import CommandLineArgsParser
from ai_model.model_handler import ModelHandler
from communicator import Communicator
from steering_command import SteeringCommand
from predicted_class import PredictedClass
from predicted_class_stack import PredictedClassStack
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

        self._predicted_class_stack = PredictedClassStack()

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
                self._start_drive()
            case _:
                print("Unknown mode. Shutting down!")


    def _model_training(self):
        self._model_handler.train_model()


    def _start_drive(self):
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
        self._turn_on_car()
        while not self._exit_flag.is_set():
            self._car_steering()

        self._turn_off_car()


    def _car_steering(self):
        response = self._communicator.take_photo()
        if response is not None:
            predicted_class = self._model_handler.classify_image(response)
            print(f"Predicted class: {predicted_class.name}")

            self._predicted_class_stack.push(predicted_class)
            self._send_commands_based_on_label(predicted_class)
        else:
            print("No response")



    def _send_commands_based_on_label(self, predicted_class: str):
        match predicted_class:
            case PredictedClass.FORWARD:
                self._communicator.send_request(SteeringCommand.FORWARD)
            case PredictedClass.BACK:
                self._communicator.send_request(SteeringCommand.BACK)
            case PredictedClass.RIGHT:
                self._communicator.send_request(SteeringCommand.RIGHT)
            case PredictedClass.LEFT:
                self._communicator.send_request(SteeringCommand.LEFT)
            case PredictedClass.SLIGHT_RIGHT:
                self._communicator.send_request(SteeringCommand.SLIGHT_RIGHT)
            case PredictedClass.SLIGHT_LEFT:
                self._communicator.send_request(SteeringCommand.SLIGHT_LEFT)
            case PredictedClass.THRASH_IMAGE:
                if self._predicted_class_stack.check_if_stack_contains_only_thrash():
                    self._communicator.send_request(SteeringCommand.STOP)
                else:
                    previous_command = self._predicted_class_stack.get_stack_second_element()
                    self._communicator.send_request(previous_command)
            case _:
                print("Unknown class predicted. Turning off robotic car.")
                self._turn_off_car()


    def _turn_on_car(self):
        self._communicator.send_request(SteeringCommand.CENTER_WHEELS)


    def _turn_off_car(self):
        self._communicator.send_request(SteeringCommand.STOP)
        self._communicator.send_request(SteeringCommand.CENTER_WHEELS)


    def _check_if_play_music(self):
        if (self._command_line_args_parser.get_music() is True and
            self._command_line_args_parser.get_mode() == 'run'):
            return True

        return False


    def _run_music_player_thread(self):
        music_player = MusicPlayer(self._exit_flag)
        music_thread = threading.Thread(target=music_player.play_music)
        music_thread.start()
        music_thread.join()
