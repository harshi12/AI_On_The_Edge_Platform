import sys
sys.path.insert (0, '../')

import argparse
import json
import time
import datetime
import numpy as np
import pandas as pd

from timer import *
from sensor import *

class EarthquakeSensor(Sensor):
    def __init__(self, dest_IP = "127.0.0.1", dest_port = 4444, rate = 0.5):
        name = "LOCATION_TIME_SENSOR"
        description = "This is an earthquake prediction sensor."
        Sensor.__init__(self, name, description, "one-way", rate, dest_IP, dest_port)

        self.dataset = pd.read_csv("./earthquake.csv").values
        self.length = self.dataset.shape[0]
        self.index = 0

    # sends simulated input to the Sensor Manager, in the prescribed rate,
    # using sockets
    def simulated_input_send(self):
        self.send_data(self.dataset[self.index][:-1].tolist(), 5556)
        self.index = (self.index + 1) % self.length


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sensor_manager_addrs", default="127.0.0.1:4444")

    (args, unknown) = parser.parse_known_args()

    sensor_manager_IP, sensor_manager_port = args.sensor_manager_addrs.split(':')

    earthquake_detect_sensor = EarthquakeSensor(sensor_manager_IP, int(sensor_manager_port))
    sensor_data_timer = RepeatedTimer(earthquake_detect_sensor.rate, earthquake_detect_sensor.simulated_input_send)
    sensor_data_timer.start()
