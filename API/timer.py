import time
from threading import Event, Thread

class RepeatedTimer:

    """Repeat `function` every `interval` seconds."""

    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.event = Event()

    def _target(self):
        while not self.event.wait(self._time):
            self.function(*self.args, **self.kwargs)

    @property
    def _time(self):
        return self.interval - ((time.time() - self.start_time) % self.interval)

    def start(self):
        actual_interval, self.interval = self.interval, 0.001
        self.start_time = time.time()
        self.thread = Thread(target=self._target)
        self.thread.start()
        self.interval = actual_interval

    def stop(self):
        self.event.set()
        self.thread.join()
