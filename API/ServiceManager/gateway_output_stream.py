import sys


from pathlib import Path
home = str(Path.home())

path = home+'/Platform/'

sys.path.insert (0, path)

import threading
import socket

import Socket.utilities as sock_util
import json
#from RabbitMQ.message_queue import *
# from queue_req_resp import *
from ServiceManager.io_stream import *

class GatewayOutputStream(IO_Stream):
    def __init__(self):
        description = "GatewayOutputStream"
        IO_Stream.__init__(self, description)

        # self.RBMQ = RabbitMQ()
        self.SERVICE_OUTPUT_QUEUE = "Service_" + self.description
        self.gateway_sockets = {}

    def handle_service_output(self, body):
        output = json.loads(body)
        #print (f"{self.description} receiving output --> {output}")

        # TODO: read config of output["service_id"] to find out where the output should go

        # OUTPUT of FLOWER_ANALYSIS_SENSOR
        # Destination: UI
        print (output)
        if output["service_id"] == "flower_svc_1":
            print ("sendind output to UI", output)
            json_output_str = json.dumps(output)
            print (f"[POS] receiving output --> {json_output_str}")
            try:
                send_to_UI_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                send_to_UI_socket.connect(("192.168.43.173",5004)) # Need to pass actual IP
                print ("send message")
                sock_util.send_msg(send_to_UI_socket, json_output_str)
            except:
                print ("UI Closed")
            
        

    # function to listen to output data from the services
    # route the data to the destinations according to configuration
    def init_output_stream(self):
        print ("calling")
        service_gateway_output_listen = socket.socket()
        service_gateway_output_listen.bind(('', 5002))
        service_gateway_output_listen.listen(15)
        print ("called")
        while True: 
            print ("getting")
            service_socket,addr = service_gateway_output_listen.accept()
            data = sock_util.recv_msg(service_socket)
            self.handle_service_output(data)
        # self.RBMQ.receive(self.handle_service_output, '', self.SERVICE_OUTPUT_QUEUE)
    
    # SERVICE APIs

    def service_output_send(self, service_id, content):
        output = {}
        output["service_id"] = service_id
        output["content"] = content
        json_output_str = json.dumps(output)

        send_to_gateway_output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_to_gateway_output_socket.connect(("127.0.0.1",5002)) # Need to pass actual IP
        sock_util.send_msg(send_to_gateway_output_socket, json_output_str)


if __name__ == "__main__":
    platform_output_stream = GatewayOutputStream()
    threading.Thread(target = platform_output_stream.init_output_stream).start()
