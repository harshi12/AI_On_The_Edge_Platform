import sensor

class SonarSensor(Sensor):
    def __init__(self, rate = 10, dest_IP = "127.0.0.1", dest_port = 4444):
        description = "This is a Naval mine sensor taking in Sonar Data."
        Sensor.__init__(self, description, "one-way", rate, dest_IP, dest_port)

    # sends simulated input to the Sensor Manager in the prescribed rate
    # use sockets
    # create thread to send simulated input
    def send_simulated_input():

if __name__ == "__main__":
    if sys.argc < 2:
        print ("Usage: sonar_sensor.py <sensor_manager_IP> <sensor_manager_port>")
        sys.exit(1)

    sonar_sensor = SonarSensor(dest_IP = sys.argv[1], dest_port = sys.argv[2])
    sonar_sensor.send_simulated_input()
