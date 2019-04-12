from sensor import *
import time
import datetime
import numpy as np
import pandas as pd
import sys
from timer import *

class SonarSensor(Sensor):
    def __init__(self, rate = 10, dest_IP = "127.0.0.1", dest_port = 4444):
        description = "This is a Naval mine sensor taking in Sonar Data."
        Sensor.__init__(self, description, "one-way", rate, dest_IP, dest_port)

        self.dataset = pd.read_csv("./Sonar.csv").values
        # dataset = dataset.values
        self.Length = self.dataset.shape[0]
        self.Index = 0
    # sends simulated input to the Sensor Manager in the prescribed rate
    # use sockets

    def send_simulated_input(self):
            print ("Time: ",datetime.datetime.now(), "---> Data: ",self.dataset[self.Index][:-1])
            self.Index = (self.Index + 1) % self.Length
        # ----- Send Output using socket ----- #

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Usage: sonar_sensor.py <sensor_manager_IP> <sensor_manager_port>")
        sys.exit(1)

    sonar_sensor = SonarSensor(dest_IP = sys.argv[1], dest_port = sys.argv[2])
    timer = RepeatedTimer(0,"SonarSensor",sonar_sensor.send_simulated_input)
    # timer = RepeatedTimer(10, sonar_sensor.send_simulated_input)
    # timer_ASAP.stop()
    # sonar_sensor.send_simulated_input()
