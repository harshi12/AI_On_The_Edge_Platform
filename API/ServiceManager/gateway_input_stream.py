import sys
sys.path.insert (0, '../')
sys.path.insert (0, '../../')

import threading
import argparse
import socket

import Socket.utilities as sock_util
#from RabbitMQ.message_queue import *
from queue_req_resp import *
from ServiceManager.io_stream import *
from Logger.logger_client import *


class GatewayInputStream(IO_Stream):
    def __init__(self):
        description = "GatewayInputStream"
        IO_Stream.__init__(self, description)

        self.RBMQ = RabbitMQ()
        self.SERVICE_REQ_QUEUE = "Service_" + self.description
        self.gateway_sockets = {}
        self.service_sockets = {}
        self.service_to_gatway_socket = None
        #self.logger = LoggerClient()

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

            input_data = json.loads(input_data)
            service_id, sensor_name, content = input_data["service_id"], input_data["sensor_name"], input_data["content"]
            # queue_name = self.description + "_" + str(service_id)
            data = {}
            data["sensor_name"] = sensor_name
            data["content"] = content
            json_data = json.dumps(data)

            sock_util.send_msg(self.service_sockets[str(service_id)], json_data)
            # Send service a data via socket
            # self.RBMQ.send("", queue_name, json_data)

    def handle_service_requests(self,body):
        req = json.loads(body)
        for gw in req["gateway_addrs"]:
            if gw not in self.gateway_sockets:
                gateway_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.gateway_sockets[gw] = gateway_sock
                gw_IP, gw_port = gw.split(':')
                gateway_sock.connect((gw_IP, int(gw_port)))
                threading.Thread(target = self.handle_input_stream, args = (gateway_sock,)).start()

            sock_util.send_msg(self.gateway_sockets[gw], body)
       

    def recv_service_requests(self):
        service_to_gateway_listen = socket.socket()
        service_to_gateway_listen.bind(('', 5001))
        service_to_gateway_listen.listen(15)
        while True: 
            service_socket,addr = service_to_gateway_listen.accept()
            data = sock_util.recv_msg(service_socket)
            req = json.loads(data)
            if str(req["service_id"]) not in self.service_sockets:
                self.service_sockets[str(req["service_id"])] = service_socket
            self.handle_service_requests(data)

        # self.RBMQ.receive(self.handle_service_requests, '', self.SERVICE_REQ_QUEUE)


    # SERVICE APIs

    # request to register service for receive data of sensor_name from gateway_addrs
    def service_register_request(self, service_id, sensor_name, input_rate):
        # get a list of gateway IP and ports from registry/... using service_id
        req = {}
        req["opcode"] = "SERVICE_REGISTER"
        req["service_id"] = service_id
        req["sensor_name"] = sensor_name
        req["input_rate"] = input_rate
        req["gateway_addrs"] = ["127.0.0.1:4445"]   # temp list of gateway IP, port
        json_req = json.dumps(req)

        self.service_to_gatway_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.service_to_gatway_socket.connect(("127.0.0.1",5001)) # Need to pass actual IP
        sock_util.send_msg(self.service_to_gatway_socket, json_req)
        # print (self.service_to_gatway_socket)
        # self.RBMQ.send("", self.SERVICE_REQ_QUEUE, json_req)


    def service_recv_input_request(self, service_id, func):
        while True:
            # print (self.service_to_gatway_socket)
            data = sock_util.recv_msg(self.service_to_gatway_socket)
            func(None,None,None,data)


if __name__ == "__main__":
    Gateway_input_stream = GatewayInputStream()
    threading.Thread(target = Gateway_input_stream.recv_service_requests).start()
