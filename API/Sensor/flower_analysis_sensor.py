import sys
from sensor import *
import time
import datetime
import numpy as np
import pandas as pd
from timer import *

class FlowerAnalysisSensor(Sensor):
    def __init__(self, rate = 0.5, dest_IP = "127.0.0.1", dest_port = 4444):
        description = "This is an iris-flower classification sensor."
        self.name = "FLOWER_ANALYSIS_SENSOR"
        Sensor.__init__(self, description, "one-way", rate, dest_IP, dest_port)

        self.dataset = pd.read_csv("./Iris.csv").values
        self.length = self.dataset.shape[0]
        self.index = 0

    # sends simulated input to the Sensor Manager, in the prescribed rate,
    # using sockets
    def send_simulated_input(self):
        flower_data = self.name + f"${self.rate}${self.dataset[self.index][:-1]}"
        self.index = (self.index + 1) % self.length

        self.send_data(flower_data)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Usage: flower_analysis_sensor.py <sensor_manager_IP> <sensor_manager_port>")
        sys.exit(1)

    flower_analysis_sensor = FlowerAnalysisSensor(dest_IP = sys.argv[1], dest_port = sys.argv[2])
    sensor_data_timer = RepeatedTimer(flower_analysis_sensor.rate, flower_analysis_sensor.send_simulated_input)
    sensor_data_timer.start()
