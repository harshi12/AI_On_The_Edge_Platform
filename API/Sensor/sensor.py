import sys
sys.path.insert(0, '../')

import json
import socket
import Socket.utilities as sock_util

class Sensor:
    # sensor_type : one-way or two way
    # rate        : input data rate in seconds
    # dest_IP     : sensor manager's IP
    # dest_port   : sensor manager's port
    def __init__(self, name, description, sensor_type, rate, dest_IP, dest_port, debug):
        self.name = name
        self.description = description
        self.sensor_type = sensor_type
        self.rate = rate
        self.dest_IP = dest_IP
        self.dest_port = int(dest_port)
        self.sock = None
        self.debug = debug

    def send_data(self, data, output_port = -1):
        if self.debug == "yes":
            print (f"Sending data: {data}")

        data_dict = {}
        data_dict["sensor_type"] = self.sensor_type
        data_dict["name"] = self.name
        data_dict["sensor_rate"] = self.rate
        data_dict["sensor_data"] = data
        data_dict["output_port"] = output_port
        json_data_str = json.dumps(data_dict)

        if self.sock:
            sock_util.send_msg(self.sock, json_data_str.encode())
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.dest_IP, self.dest_port))
        sock_util.send_msg(sock, json_data_str.encode())

        if self.rate < 5:
            self.sock = sock
        else:
            sock.close()
            self.sock = None
 
