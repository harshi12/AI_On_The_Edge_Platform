import sys
sys.path.insert(0, '../')

import threading
import socket
import json
import Socket.utilities as sock_util

from timer import *

class SensorManager:
    def __init__(self, IP = "127.0.0.1", sensor_port = 4444, service_port = 4445):
        self.IP = IP
        self.sensor_port = sensor_port
        self.service_port = service_port
        self.supported_sensors = {}
        self.sensor_rates = {}
        self.sensor_buffer = {}
        self.sensor_buffer_lock = {}
        self.service_input_timers = {}
        self.platform_input_sock = None
        self.gateway_input_sock = None


    # separate thread for each sensor type
    # sensor data will be received in this thread
    def input_stream(self, sensor_sock):
        while True:
            sensor_input = sock_util.recv_msg(sensor_sock)
            if sensor_input == None:
                print ("Sensor stopped!!")
                break

            if not isinstance(sensor_input, str):
                sensor_input = sensor_input.decode()

            sensor_input = json.loads(sensor_input)
            sensor_type, sensor_rate, sensor_data = sensor_input["sensor_type"], sensor_input["sensor_rate"], sensor_input["sensor_data"]
            if sensor_type not in self.supported_sensors:
                print (f"Registering Sensor Type: {sensor_type} --> data: {sensor_data}")
                self.sensor_rates[sensor_type] = sensor_rate
                self.supported_sensors[sensor_type] = sensor_sock
                self.sensor_buffer[sensor_type] = []
                self.sensor_buffer_lock[sensor_type] = threading.Lock()

                with self.sensor_buffer_lock[sensor_type]:
                    self.sensor_buffer[sensor_type].append(sensor_data)

                # TODO: write this new sensor to the sensor config file
            else:
                with self.sensor_buffer_lock[sensor_type]:
                    self.sensor_buffer[sensor_type][0] = sensor_data


    def handle_sensors(self):
        self.sensor_mgr_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sensor_mgr_sock.bind((self.IP, self.sensor_port))
        self.sensor_mgr_sock.listen(5)

        while True:
            sensor_sock, sensor_address = self.sensor_mgr_sock.accept()
            t1 = threading.Thread(target = self.input_stream, args = (sensor_sock,))
            t1.start()

        self.sensor_mgr_sock.close()


    def send_input_to_service(self, service_sock, service_id, sensor_type):
        with self.sensor_buffer_lock[sensor_type]:
            sensor_data = self.sensor_buffer[sensor_type][0]

        input_data_dict = {}
        input_data_dict["service_id"] = str(service_id)
        input_data_dict["sensor_type"] = str(sensor_type)
        input_data_dict["content"] = str(sensor_data)
        json_data_str = json.dumps(input_data_dict)

        print ("Sending input data to service -->", json_data_str)
        sock_util.send_msg(service_sock, json_data_str.encode())


    # service_sock: platform input stream socket
    # service request will be received on this socket
    def handle_service_commands(self, service_sock):
        while True:
            service_req = sock_util.recv_msg(service_sock)
            if service_req == None:
                break

            if not isinstance(service_req, str):
                service_req = service_req.decode()

            req = json.loads(service_req)
            #print ("SENSOR_MANAGER received service request:", service_req)
            opcode, service_id, sensor_type, input_rate = req["opcode"], req["service_id"], req["sensor_type"], req["input_rate"]
            if opcode == "SERVICE_REGISTER":
                if service_id not in self.service_input_timers:
                    if input_rate == "default_rate":
                        timer = RepeatedTimer(float(self.sensor_rates[sensor_type]), self.send_input_to_service, service_sock, service_id, sensor_type)
                    else:
                        timer = RepeatedTimer(float(input_rate), self.send_input_to_service, service_sock, service_id, sensor_type)
                    timer.start()
                    self.service_input_timers[service_id] = timer
            elif opcode == "SERVICE_UNREGISTER":
                if service_id in service_input_timers:
                    self.service_input_timers[service_id].stop()
                    self.service_input_timers.pop(service_id, None)
            else:
                print ("Shouldn't reach here!!")
                pass

    # separate thread for listening to incoming services
    # register and unregister a service for receiving data from a particular sensor type
    def handle_services(self):
        self.service_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.service_sock.bind((self.IP, self.service_port))
        self.service_sock.listen(5)

        while True:
            service_sock, service_address = self.service_sock.accept()
            t1 = threading.Thread(target = self.handle_service_commands, args = (service_sock,))
            t1.start()

        self.service_sock.close()


    # route the output data to the appropriate sensor
    def output_stream(self):
        pass

if __name__ == "__main__":
    sensor_manager = SensorManager()

    threading.Thread(target = sensor_manager.handle_sensors).start()
    threading.Thread(target = sensor_manager.handle_services).start()
