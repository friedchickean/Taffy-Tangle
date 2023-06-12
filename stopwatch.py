# step 0: declare our class name
import math
import time


class Stopwatch:

    # step 1: define a constructor
    def __init__(self):
        """
        Set up the initial state of my object
        """
        # instance variable to keep track of elasped time
        self._elapsed_time = 0.0

        # instance var to remember when we started the watch
        self._start_time = 0.0

    # step 2: define methods (operations) for using a stopwatch

    def start(self):
        # remember the time we hit start for later
        self._start_time = time.time()

    def stop(self):
        # add to the elapsed time, the time btw now and when we started
        dt = time.time() - self._start_time
        self._elapsed_time += dt

    def lap(self):
        pass

    def reset(self):
        self._elapsed_time = 0.0

    def elapsed(self):
        """
        :return:
        """
        return self._elapsed_time


# test code!
if __name__ == "__main__":
    # create the stopwatch
    timer = Stopwatch()
    # time how long it takes to compute 100000 square roots?
    timer.start()
    for i in range(100000):
        math.sqrt(float(i))
    timer.stop()

    seconds = timer.elapsed()
    print('It took ', str(seconds), ' to compute!')
