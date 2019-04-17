import sys
sys.path.insert(0, '../')

import time
import datetime
import numpy as np
import pandas as pd
import argparse

from timer import *
from sensor import *

class SonarSensor(Sensor):
    def __init__(self, debug, dest_IP = "127.0.0.1", dest_port = 4444, rate = 10):
        name = "SONAR_SENSOR"
        description = "This is a Naval mine sensor taking in Sonar Data."
        Sensor.__init__(self, name, description, "one-way", rate, dest_IP, dest_port, debug)

        self.dataset = pd.read_csv("./Sonar.csv").values
        self.length = self.dataset.shape[0]
        self.index = 0

    # sends simulated input to the Sensor Manager, in the prescribed rate
    # using sockets
    def simulated_input_send(self):
        self.send_data(self.dataset[self.index][:-1].tolist(), 5555)
        self.index = (self.index + 1) % self.length


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sensor_manager_addrs", default="127.0.0.1:4444")
    parser.add_argument("--debug", default="no")

    (args, unknown) = parser.parse_known_args()
    sensor_manager_IP, sensor_manager_port = args.sensor_manager_addrs.split(':')

    sonar_sensor = SonarSensor(args.debug, sensor_manager_IP, int(sensor_manager_port))
    sensor_data_timer = RepeatedTimer(sonar_sensor.rate, sonar_sensor.simulated_input_send)
    sensor_data_timer.start()
