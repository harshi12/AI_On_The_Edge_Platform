import sys
sys.path.insert (0, '../')

import threading
import argparse
import socket

import Socket.utilities as sock_util
from RabbitMQ.message_queue import *
from ServiceManager.io_stream import *

class PlatformInputStream(IO_Stream):
    def __init__(self):
        description = "PlatformInputStream"
        IO_Stream.__init__(self, description)

        self.RBMQ = RabbitMQ()
        self.SERVICE_REQ_QUEUE = "Service_" + self.description
        self.gateway_sockets = {}

    # function to listen to input data from the sensor manager
    # route the data to the appropriate service
    def handle_input_stream(self, gateway_sock):
        while True:
            input_data = sock_util.recv_msg(gateway_sock)
            if input_data is None:
                print ("Connection with gateway lost!!")
                break

            if not isinstance(input_data, str):
                input_data = input_data.decode()

            # find an appropriate service queue according to load balancer!!!
            input_data = json.loads(input_data)
            service_id, sensor_type, content = input_data["service_id"], input_data["sensor_type"], input_data["content"]
            queue_name = self.description + "_" + str(service_id)
            data = {}
            data["sensor_type"] = sensor_type
            data["content"] = content
            json_data = json.dumps(data)
            self.RBMQ.send("", queue_name, json_data)
        

    def recv_input_content(self, service_id, func):
        self.RBMQ.receive(func, '', self.description + "_" + str(service_id))

    def recv_service_requests(self):
        self.RBMQ.receive(self.handle_service_requests, '', self.SERVICE_REQ_QUEUE)


    def handle_service_requests(self, ch, method, properties, body):
        req = json.loads(body)
        for gw in req["gateway_addrs"]:
            if gw not in self.gateway_sockets:
                gateway_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.gateway_sockets[gw] = gateway_sock
                gw_IP, gw_port = gw.split(':')
                gateway_sock.connect((gw_IP, int(gw_port)))
                threading.Thread(target = self.handle_input_stream, args = (gateway_sock,)).start()


            sock_util.send_msg(self.gateway_sockets[gw], body)


    # request to register service for receive data of sensor_type from gateway_addrs
    def service_register_request(self, service_id, sensor_type, input_rate):
        # get a list of gateway IP and ports from registry/... using service_id
        req = {}
        req["opcode"] = "SERVICE_REGISTER"
        req["service_id"] = service_id
        req["sensor_type"] = sensor_type
        req["input_rate"] = input_rate
        req["gateway_addrs"] = ["127.0.0.1:4445"]   # temp list of gateway IP, port
        json_req = json.dumps(req)
        self.RBMQ.send("", self.SERVICE_REQ_QUEUE, json_req)


if __name__ == "__main__":
    platform_input_stream = PlatformInputStream()
    threading.Thread(target = platform_input_stream.recv_service_requests).start()
