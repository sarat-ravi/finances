import time as real_time

class Timer(object):

    def __init__(self):
        super(Timer, self).__init__()

    def time(self):
        # TODO(Sarat): Allow to customize the timer
        return real_time.time()

TIMER = Timer()

def time():
    return TIMER.time()
