class Sensor:
    # sensor_type : one-way or two way
    # rate        : input data rate in seconds
    # dest_IP     : sensor manager's IP
    # dest_port   : sensor manager's port
    def __init__(self, description, sensor_type, rate = 1, dest_IP = "127.0.0.1", dest_port = 4444):
        self.description = description
        self.sensor_type = sensor_type
        self.rate = rate
        self.dest_IP = d_IP
        self.dest_port = dest_port


