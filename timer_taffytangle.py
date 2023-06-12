"""
timer class
Heavily inspired by Prof. Chan's "stopwatch.py" in-class example
"""

import math
import time


class Timer:

    def __init__(self):
        self._elapsed_time = 0.0
        self._final_time = 0.0
        self._start_time = 0.0
        self._current_time = 0.0

    def start_timer(self):
        self._start_time = time.time()

    def time_elapsed(self):
        elapsed_time = time.time() - self._start_time
        return int(round(elapsed_time))

    def stop(self):
        dt = time.time() - self._start_time
        self._final_time += dt

    def reset(self):
        self._elapsed_time = 0.0
        self._current_time = 0.0


