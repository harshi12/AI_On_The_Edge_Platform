import sys
from sensor import *

class FlowerSensor(Sensor):
    def __init__(self, rate = 0.5, dest_IP = "127.0.0.1", dest_port = 5555):
        description = "This is an iris-flower classification sensor."
        Sensor.__init__(self, description, "one-way", rate, dest_IP, dest_port)


if __name__ == "__main__":
    if sys.argc < 2:
        print ("Usage: flower_sensor.py <sensor_manager_IP> <sensor_manager_port>")
        sys.exit(1)

    flower_sensor = FlowerSensor(dest_IP = sys.argv[1], dest_port = sys.argv[2])
