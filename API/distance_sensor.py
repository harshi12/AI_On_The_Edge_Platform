import sys
from sensor import *
from random import choices
import random 
import time
import datetime
import _thread

class DistanceSensor(Sensor):
    def __init__(self, rate = 1, dest_IP = "127.0.0.1", dest_port = 4444):
        description = "This sensor is a distance sensor and is deployed on the base of the submarine."+"This captures the distance of the submarine from the land below."
        Sensor.__init__(self, description, "two-way", rate, dest_IP, dest_port)

    # sends simulated input to the Sensor Manager in the prescribed rate
    # use sockets
    # create thread to send simulated input
    def send_simulated_input(self):
        x = 0
        while(x < 5):
            Time = 
            population = [0,1]
            weights = [0.1, 0.9]
            Number_Selected = choices(population, weights)
            Generated_Distance = None
            if(Number_Selected[0]):
                Generated_Distance = random.randint(201,1001)
            else:
                Generated_Distance = random.randint(0,201)
            print ("Time: ",datetime.datetime.now(), "---> Generated_Distance: ",Generated_Distance)
            time.sleep(1)
            #-------------- Send Generated_Distance using socket ------------- #

    # receive display alarm service's output using sockets
    def receive_alarm_output(self):
        print ("Time: ",datetime.datetime.now(),"Receive Call")
        #-------------- Receive output using socket ------------- #
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Usage: distance_sensor.py <sensor_manager_IP> <sensor_manager_port>")
        sys.exit(1)

    distance_sensor = DistanceSensor(dest_IP = sys.argv[1], dest_port = sys.argv[2])

    print ("Starting send_simulated_input thread and receive_alarm_output Function")
    try:
        _thread.start_new_thread(distance_sensor.send_simulated_input,())
    except:
        print ("Error: unable to start thread")
        sys.exit(1)
    print ("send_simulated_input thread started")

    print ("Starting receive_alarm_output function")
    distance_sensor.receive_alarm_output()
    print ("Receive_alarm_output function started")

    while 1:
        pass


