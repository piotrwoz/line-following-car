"""
CommandLineArgsParser class is responsible for parsing and validating user arguments from
command line.
"""

import sys
import argparse


class CommandLineArgsParser:
    """
    CommandLineArgsParser class is parser and validator for user's arguments from command line.
    """
    def __init__(self):
        app_description = self._prepare_app_description()
        self._parser = argparse.ArgumentParser(description=app_description)

        help_descriptions = self._prepare_help_for_arguments()
        self._parser.add_argument("--mode", type=str, required=True, help=help_descriptions[0])
        self._parser.add_argument("--epochs", type=int, required=False, help=help_descriptions[1])
        self._parser.add_argument("--batch", type=int, required=False, help=help_descriptions[2])
        self._parser.add_argument("--time", type=int, required=False, help=help_descriptions[3])
        self._parser.add_argument("--model", type=str, required=False, help=help_descriptions[4])
        self._parser.add_argument("--music", type=str, required=False, help=help_descriptions[5])
        self._args = self._parser.parse_args()

        try:
            self._map_music_arg()
        except argparse.ArgumentTypeError as ex:
            print(ex)
            print("No music will be played")
        self._validate_args()


    def _prepare_app_description(self) -> str:
        description = '''Software for line following robotic car. This main app is using
        for starting car and training neural network model'''

        return description


    def _prepare_help_for_arguments(self) -> (str, str, str, str, str, str):
        mode_help = """Specify mode of application. Allowed values: 'run', or 'train'.
        Argument required."""
        epochs_help = """Specify training epochs amount. Required only when mode is 'train'.
        Must be positive integer."""
        batch_help = """Specify batch size. Required only when mode is 'train'.
        Positive integer required."""
        time_help = """Specify time of driving robotic-car in seconds. Positive integer required"""
        model_help = """Specify name of the trained neural network model for use.
        It has to be *.pt file. File with trained model should be stored in
        ./src/ai_model_trained_models/ directory"""
        music_help = """Specify if music should be played when car is started.
        Possible values: 'true'/'on' or 'false'/'off'"""

        return(mode_help, epochs_help, batch_help, time_help, model_help, music_help)


    def _map_music_arg(self) -> bool:
        if not self._args.music or self._args.music.lower() in ('false', 'off'):
            self._args.music = False
        elif self._args.music.lower() in ('true', 'on'):
            self._args.music = True
        else:
            exception_str = "'true', 'on', 'false' or 'off' argument value expected"
            self._args.music = False
            raise argparse.ArgumentTypeError(exception_str)


    def _validate_args(self):
        is_error = False
        if self._args.mode.lower() not in ('run', 'train'):
            print("Wrong mode param. It has to 'run' or 'train'.")
            is_error = is_error or True
        else:
            if self._args.mode.lower() == 'train':
                is_error = self._validate_train_args()
            if self._args.mode.lower() == 'run':
                is_error = self._validate_run_args()

            if is_error:
                print("Wrong user's arguments. Shutting down!")
                sys.exit(1)


    def _validate_train_args(self) -> bool:
        is_error = False
        if not self._args.epochs:
            print("No epochs amount param! Specify epochs number.")
            is_error = True
        elif self._args.epochs < 0:
            print("Wrong epochs amount param! It has to be positive integer number.")
            is_error = True

        if not self._args.batch:
            print("No batch size param! Specify batch size.")
            is_error = True
        elif self._args.batch < 0:
            print("Wrong batch size param. It has to be positive integer number.")
            is_error = True

        return is_error


    def _validate_run_args(self) -> bool:
        is_error = False
        if not self._args.time:
            print("No time param. Specify time of app's work as positive integer number.")
            is_error = True
        elif self._args.time < 0:
            print("Wrong time param. It has to be positive integer number.")
            is_error = True

        if not self._args.model or self._args.model == "":
            print("No model file name param. Specify trained model.")
            is_error = True

        return is_error

    def get_mode(self):
        """
        Mode getter.
        """
        return self._args.mode


    def get_epochs(self):
        """
        Epochs amount getter.
        """
        return self._args.epochs


    def get_batch(self):
        """
        Batch size getter.
        """
        return self._args.batch


    def get_time(self):
        """
        Time getter.
        """
        return self._args.time

    def get_model(self):
        """
        Trained model getter.
        """
        return self._args.model


    def get_music(self):
        """
        Music getter.
        """
        return self._args.music


    def print_args(self):
        """
        Print command line arguments on console.
        """
        if self._args.mode == "run":
            print(f"App mode: {self._args.mode}")
            print(f"Time: {self._args.time}")
            print(f"Model: {self._args.model}")
            print(f"If music: {self._args.music}")
        if self._args.mode == "train":
            print(f"App mode: {self._args.mode}")
            print(f"Epochs: {self._args.epochs}")
            print(f"Batch size: {self._args.batch}")


if __name__ == "__main__":
    command_line_parser = CommandLineArgsParser()
    command_line_parser.print_args()
