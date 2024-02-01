"""
Timer class.
"""

import threading
import sys
import time


class Timer:
    """
    Timer class is responsible for counting time of application runtime
    and setting proper flag when given time of runtime is out. It should
    be tun in non-main thread.
    """

    def __init__(self, time_to_count: int, exit_flag: threading.Event):
        self._exit_flag = exit_flag
        self._time_to_count = time_to_count

    def start_timer(self):
        """Start time counting. When time is out, proper exit flag is set."""
        print(f"Timer has started. Time to count: {self._time_to_count}")
        time.sleep(self._time_to_count)
        print("Time is out.")

        self._exit_flag.set()
        sys.exit()
