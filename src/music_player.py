"""
Music player class manages audio playing during robotic car drive.
"""

import threading
import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from settings_readers.drive_settings_reader import DriveSettingsReader


class MusicPlayer:
    """
    MusicPlayer class is responsible for playing specific soundtrack during robotic car drive.
    """

    def __init__(self, exit_flag: threading.Event):
        self._exit_flag = exit_flag


    def play_music(self):
        """Start playing music"""
        drive_settings_reader = DriveSettingsReader()
        drive_settings_reader.read()

        forward_speed = drive_settings_reader.get_standard_forward()
        max_forward_speed = drive_settings_reader.get_max_forward()
        music_file_path = None
        if forward_speed >= max_forward_speed / 2:
            music_file_path = "../../sound/max_verstappen_song.mp3"
        else:
            music_file_path = "../../sound/drive_main_theme.mp3"

        pygame.mixer.init()
        pygame.mixer.music.load(music_file_path)
        pygame.mixer.music.play(-1)

        sys.exit()
