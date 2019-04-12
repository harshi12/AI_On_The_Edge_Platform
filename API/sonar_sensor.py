import sensor

class SonarSensor(Sensor):
    def __init__(self, rate = 10, dest_IP = "127.0.0.1", dest_port = 4444):
        description = "This is a Naval mine sensor taking in Sonar Data."
        Sensor.__init__(self, description, "one-way", rate, dest_IP, dest_port)


if __name__ == "__main__":
    if sys.argc < 2:
        print ("Usage: sonar_sensor.py <sensor_manager_IP> <sensor_manager_port>")
        sys.exit(1)

    sonar_sensor = SonarSensor(dest_IP = sys.argv[1], dest_port = sys.argv[2])
