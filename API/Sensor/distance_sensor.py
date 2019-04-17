import sys
sys.path.insert(0, '../')

import argparse
from random import choices
import random 
import time
import datetime
import _thread
import threading 

from timer import *
from sensor import *

class DistanceSensor(Sensor):
    def __init__(self, debug, dest_IP = "127.0.0.1", dest_port = 4444, rate = 1):
        description = "This sensor is a distance sensor and is deployed on the base of the submarine. This captures the distance of the submarine from the land below."
        name = "DISTANCE_SENSOR"
        Sensor.__init__(self, name, description, "two-way", rate, dest_IP, dest_port, debug)


    # sends simulated input to the Sensor Manager, in the prescribed rate,
    # using sockets
    def simulated_input_send(self):
        population = [0, 1]
        weights = [0.1, 0.9]
        Number_Selected = choices(population, weights)
        distance_data = None

        if(Number_Selected[0]):
            distance = random.randint(201, 1001)
        else:
            distance = random.randint(0, 201)

        self.send_data(distance, 5557)


    # receive display alarm service's output using sockets
    def receive_alarm_output(self):
        while True:
            if self.sock == None:
                continue

            output_content = sock_util.recv_msg(self.sock)
            if output_content == None:
                print ("[Distance Sensor] Output connection with Sensor Manager lost!!")
                break

            if not isinstance(output_content, str):
                output_content = output_content.decode()
            
            json_output = json.loads(output_content)
            print ("[Distance Sensor]", json_output["content"])
        # print ("Time: ",datetime.datetime.now(),"Receive Call")
        #-------------- Receive output using socket ------------- #


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sensor_manager_addrs", default="127.0.0.1:4444")
    parser.add_argument("--debug", default="no")

    (args, unknown) = parser.parse_known_args()
    sensor_manager_IP, sensor_manager_port = args.sensor_manager_addrs.split(':')

    distance_sensor = DistanceSensor(args.debug, sensor_manager_IP, int(sensor_manager_port))

    # send simulated data at the prescribed rate
    sensor_data_timer = RepeatedTimer(distance_sensor.rate, distance_sensor.simulated_input_send)
    sensor_data_timer.start()

    threading.Thread(target = distance_sensor.receive_alarm_output).start()
