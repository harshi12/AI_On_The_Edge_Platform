import sys
sys.path.insert(0, '../')

import threading
import socket
import Socket.utilities as sock_util

class SensorManager:
    def __init__(self, IP = "127.0.0.1", port = 4444):
        self.IP = IP
        self.port = port
        self.supported_sensors = {}
        self.sensor_buffer = {}
        self.sensor_buffer_lock = {}

    def receive_sensor_data(self, sensor_sock):
        while True:
            sensor_input = sock_util.recv_msg(sensor_sock)
            if sensor_input == None:
                break

            if not isinstance(sensor_input, str):
                sensor_input = sensor_input.decode()

            sensor_type, sensor_data = sensor_input.split('$')
            if sensor_type not in self.supported_sensors:
                print (f"Registering Sensor Type: {sensor_type} --> data: {sensor_data}")
                self.supported_sensors[sensor_type] = sensor_sock
                self.sensor_buffer[sensor_type] = []
                self.sensor_buffer_lock[sensor_type] = threading.Lock()

                with self.sensor_buffer_lock[sensor_type]:
                    self.sensor_buffer[sensor_type].append(sensor_data)

                # TODO: write this new sensor to the sensor config file
            else:
                print (f"Receiving data, Sensor Type: {sensor_type} --> data: {sensor_data}")
                with self.sensor_buffer_lock[sensor_type]:
                    self.sensor_buffer[sensor_type][0] = sensor_data


    def handle_sensors(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.IP, self.port))
        self.sock.listen(5)

        while True:
            sensor_sock, sensor_address = self.sock.accept()
            t1 = threading.Thread(target = self.receive_sensor_data, args = (sensor_sock,))
            t1.start()

        self.sock.close()

    
    # separate thread for each sensor type
    # sensor data will be received in this thread
    def input_stream(self, sensor_type):
        pass

    # separate thread for listening to incoming services
    # register and unregister a service for receiving data from a particular sensor type
    def listen_services(self):
        pass

    # route the output data to the appropriate sensor
    def output_stream(self):
        pass

if __name__ == "__main__":
    sensor_manager = SensorManager()

    t1 = threading.Thread(target = sensor_manager.handle_sensors)
    t1.start()

    sensor_manager.listen_services()
