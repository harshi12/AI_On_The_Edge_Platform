import sys
from sensor import *

class FlowerAnalysisSensor(Sensor):
    def __init__(self, rate = 0.5, dest_IP = "127.0.0.1", dest_port = 4444):
        description = "This is an iris-flower classification sensor."
        Sensor.__init__(self, description, "one-way", rate, dest_IP, dest_port)

    # sends simulated input to the Sensor Manager in the prescribed rate
    # use sockets
    def send_simulated_input():


if __name__ == "__main__":
    if sys.argc < 2:
        print ("Usage: flower_analysis_sensor.py <sensor_manager_IP> <sensor_manager_port>")
        sys.exit(1)

    flower_analysis_sensor = FlowerAnalysisSensor(dest_IP = sys.argv[1], dest_port = sys.argv[2])
    flower_analysis_sensor.send_simulated_input()
