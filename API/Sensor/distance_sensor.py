import sys
sys.path.insert(0, '../')

from sensor import *
from random import choices
import random 
import time
import datetime
import _thread
import threading 
from timer import *

class DistanceSensor(Sensor):
    def __init__(self, rate = 1, dest_IP = "127.0.0.1", dest_port = 4444):
        description = "This sensor is a distance sensor and is deployed on the base of the submarine. This captures the distance of the submarine from the land below."
        self.name = "DISTANCE_SENSOR"
        Sensor.__init__(self, description, "two-way", rate, dest_IP, dest_port)

    # sends simulated input to the Sensor Manager, in the prescribed rate,
    # using sockets
    def send_simulated_input(self):
        population = [0, 1]
        weights = [0.1, 0.9]
        Number_Selected = choices(population, weights)
        distance_data = None

        if(Number_Selected[0]):
            distance = random.randint(201, 1001)
        else:
            distance = random.randint(0, 201)

        distance_data = self.name + f"${distance}"

        self.send_data(distance_data)


    # receive display alarm service's output using sockets
    def receive_alarm_output(self):
        pass
        # print ("Time: ",datetime.datetime.now(),"Receive Call")
        #-------------- Receive output using socket ------------- #


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Usage: distance_sensor.py <sensor_manager_IP> <sensor_manager_port>")
        sys.exit(1)

    distance_sensor = DistanceSensor(dest_IP = sys.argv[1], dest_port = sys.argv[2])

    # send simulated data at the prescribed rate
    sensor_data_timer = RepeatedTimer(distance_sensor.rate, distance_sensor.send_simulated_input)
    sensor_data_timer.start()

    distance_sensor.receive_alarm_output()
