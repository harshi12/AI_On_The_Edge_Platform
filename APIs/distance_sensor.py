import sys
from sensor import *

class DistanceSensor(Sensor):
    def __init__(self, rate = 1, dest_IP = "127.0.0.1", dest_port = 4444):
        description = "This sensor is a distance sensor and is deployed on the base of the submarine."
                      "This captures the distance of the submarine from the land below."
        Sensor.__init__(self, description, "two-way", rate, dest_IP, dest_port)

    # sends simulated input to the Sensor Manager in the prescribed rate
    # use sockets
    # create thread to send simulated input
    def send_simulated_input():

    # receive display alarm service's output using sockets
    def receive_alarm_output():

if __name__ == "__main__":
    if sys.argc < 2:
        print ("Usage: distance_sensor.py <sensor_manager_IP> <sensor_manager_port>")
        sys.exit(1)

    distance_sensor = DistanceSensor(dest_IP = sys.argv[1], dest_port = sys.argv[2])
    distance_sensor.send_simulated_input()
    distance_sensor.receive_alarm_output()


