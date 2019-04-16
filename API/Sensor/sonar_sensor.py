from sensor import *
import time
import datetime
import numpy as np
import pandas as pd
import sys

from timer import *

class SonarSensor(Sensor):
    def __init__(self, rate = 10, dest_IP = "127.0.0.1", dest_port = 4444):
        name = "SONAR_SENSOR"
        description = "This is a Naval mine sensor taking in Sonar Data."
        Sensor.__init__(self, name, description, "one-way", rate, dest_IP, dest_port)

        self.dataset = pd.read_csv("./Sonar.csv").values
        self.length = self.dataset.shape[0]
        self.index = 0

    # sends simulated input to the Sensor Manager, in the prescribed rate
    # using sockets
    def simulated_input_send(self):
        self.send_data(self.dataset[self.index][:-1].tolist())
        self.index = (self.index + 1) % self.length


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Usage: sonar_sensor.py <sensor_manager_IP> <sensor_manager_port>")
        sys.exit(1)

    sonar_sensor = SonarSensor(dest_IP = sys.argv[1], dest_port = sys.argv[2])
    sensor_data_timer = RepeatedTimer(sonar_sensor.rate, sonar_sensor.simulated_input_send)
    sensor_data_timer.start()
