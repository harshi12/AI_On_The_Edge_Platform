import sys
sys.path.insert(0, '../')

import threading
import socket
import json
import Socket.utilities as sock_util

from timer import *

class SensorManager:
    def __init__(self, IP = "127.0.0.1", sensor_port = 4444, service_port = 4445, output_port = 4446):
        self.IP = IP
        self.sensor_port = sensor_port
        self.service_port = service_port
        self.output_port = output_port
        self.supported_sensors = {}
        self.output_sensor_sock = {}
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
                break

            if not isinstance(sensor_input, str):
                sensor_input = sensor_input.decode()

            sensor_input = json.loads(sensor_input)
            sensor_name, sensor_type, sensor_rate, sensor_data = sensor_input["name"], sensor_input["sensor_type"], sensor_input["sensor_rate"], sensor_input["sensor_data"]
            if sensor_name not in self.supported_sensors:
                print (f"Registering Sensor Name: {sensor_name} --> data: {sensor_data}")
                self.sensor_rates[sensor_name] = sensor_rate
                self.supported_sensors[sensor_name] = sensor_sock
                self.sensor_buffer[sensor_name] = []
                self.sensor_buffer_lock[sensor_name] = threading.Lock()

                with self.sensor_buffer_lock[sensor_name]:
                    self.sensor_buffer[sensor_name].append(sensor_data)

                #if sensor_type == "two-way":
                if False:
                    sensor_IP = "127.0.0.1"
                    sensor_output_port = int(sensor_input["output_port"])
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((sensor_IP, sensor_output_port))
                    self.output_sensor_sock[sensor_name] = sock


                # TODO: write this new sensor to the sensor config file
            else:
                with self.sensor_buffer_lock[sensor_name]:
                    self.sensor_buffer[sensor_name][0] = sensor_data


    def handle_sensors(self):
        self.sensor_mgr_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sensor_mgr_sock.bind((self.IP, self.sensor_port))
        self.sensor_mgr_sock.listen(5)

        while True:
            sensor_sock, sensor_address = self.sensor_mgr_sock.accept()
            t1 = threading.Thread(target = self.input_stream, args = (sensor_sock,))
            t1.start()

        self.sensor_mgr_sock.close()


    def send_input_to_service(self, service_sock, service_id, sensor_name):
        with self.sensor_buffer_lock[sensor_name]:
            sensor_data = self.sensor_buffer[sensor_name][0]

        input_data_dict = {}
        input_data_dict["service_id"] = str(service_id)
        input_data_dict["sensor_name"] = str(sensor_name)
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
            opcode, service_id, sensor_name, input_rate = req["opcode"], req["service_id"], req["sensor_name"], req["input_rate"]
            if opcode == "SERVICE_REGISTER":
                if service_id not in self.service_input_timers:
                    if input_rate == "default_rate":
                        timer = RepeatedTimer(float(self.sensor_rates[sensor_name]), self.send_input_to_service, service_sock, service_id, sensor_name)
                    else:
                        timer = RepeatedTimer(float(input_rate), self.send_input_to_service, service_sock, service_id, sensor_name)
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
            threading.Thread(target = self.handle_service_commands, args = (service_sock,)).start()

        self.service_sock.close()


    def handle_output_content(self, output_sock):
        while True:
            output_content = sock_util.recv_msg(output_sock)
            if output_content == None:
                print("[SensorManager] Output connection with platform lost!!")
                break

            if not isinstance(output_content, str):
                output_content = output_content.decode()

            output_dict = json.loads(output_content)

            print ("[SensorManager] receiving output --> ", output_dict)
            sock_util.send_msg(self.supported_sensors[output_dict["sensor_name"]], output_content)


    # route the output data to the appropriate sensor
    def init_output_stream(self):
        self.output_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.output_sock.bind((self.IP, self.output_port))
        self.output_sock.listen(5)

        while True:
            output_sock, service_address = self.output_sock.accept()
            threading.Thread(target = self.handle_output_content, args = (output_sock,)).start()

        self.output_sock.close()


if __name__ == "__main__":
    sensor_manager = SensorManager()

    threading.Thread(target = sensor_manager.handle_sensors).start()
    threading.Thread(target = sensor_manager.handle_services).start()
    threading.Thread(target = sensor_manager.init_output_stream).start()
