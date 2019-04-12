import time
from threading import Event, Thread

class RepeatedTimer:

    """Repeat `function` every `interval` seconds."""

    def __init__(self, interval,class_name, function, *args, **kwargs):
        self.class_name = class_name
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start = time.time()
        self.event = Event()
        self.thread = Thread(target=self._target)
        self.thread.start()
        if (self.class_name == "DistanceSensor"):
            self.interval = 1
        elif (self.class_name == "SonarSensor"):
            self.interval = 10
        else:
            self.interval = 0.5

    def _target(self):
        while not self.event.wait(self._time):
            self.function(*self.args, **self.kwargs)

    @property
    def _time(self):
        if (not self.interval):
            return 0
        return self.interval - ((time.time() - self.start) % self.interval)

    def stop(self):
        self.event.set()
        self.thread.join()


# start timer
# timer = RepeatedTimer(1, print, 'Hello world')

# stop timer
# timer.stop()
