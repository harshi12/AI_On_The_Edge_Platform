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
        Sensor.__init__(self, description, "one-way", rate, dest_IP, dest_port)

        self.dataset = pd.read_csv("./Iris.csv").values
        self.Length = self.dataset.shape[0]
        self.Index = 0

    # sends simulated input to the Sensor Manager in the prescribed rate
    # use sockets
    def send_simulated_input(self):
        print ("Time: ",datetime.datetime.now(), "---> Data: ",self.dataset[self.Index][:-1])
        self.Index = (self.Index + 1) % self.Length
        # ----------- send data using socket programming ----------- #

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Usage: flower_analysis_sensor.py <sensor_manager_IP> <sensor_manager_port>")
        sys.exit(1)

    flower_analysis_sensor = FlowerAnalysisSensor(dest_IP = sys.argv[1], dest_port = sys.argv[2])
    timer = RepeatedTimer(0,"FlowerAnalysisSensor",flower_analysis_sensor.send_simulated_input)
    # flower_analysis_sensor.send_simulated_input()
