import sys

from pathlib import Path
home = str(Path.home())
path = home+'/Platform/'

sys.path.insert (0, path)

import threading
import socket

import Socket.utilities as sock_util
from queue_req_resp import *
from ServiceManager.io_stream import *
from db_client import *

class PlatformOutputStream(IO_Stream):
    def __init__(self):
        description = "PlatformOutputStream"
        IO_Stream.__init__(self, description)

        self.RBMQ = RabbitMQ()
        self.SERVICE_OUTPUT_QUEUE = "Service_" + self.description
        self.gateway_sockets = {}

    def handle_service_output(self, ch, method, properties, body):
        output = json.loads(body)
        #print (f"{self.description} receiving output --> {output}")

        # TODO: read config of output["service_id"] to find out where the output should go

        service_id = output["service_id"]

        db = DATABASE_CLIENT()
        db_response = db.service_name_get(service_id)
        if not isinstance(db_response, str):
            db_response = db_response.decode()

        service_name = None
        if service_id != "flower_svc_1" and service_id != "sonar_svc_1" and service_id != "earthquake_svc_1":
            db_response = json.loads(db_response)
            print ("[POS] Receiving ", db_response)
            db_response = db_response["response"]
            service_name = db_response["service_id"]

        # OUTPUT of DISTANCE_ALARM_SERVICE
        # Destination: DISTANCE_SENSOR
        #if service_id == "dist_svc_1":
        if service_name == "Distance_Alarm_Service":
            output["sensor_name"] = "DISTANCE_SENSOR"
            # it has to send the result back to the sensor
            # get list of gateways where this sensor is running
            gateway_addrs = ["127.0.0.1:4446"]    # temp list of gateways, currently only 1 gateway
            for gw in gateway_addrs:
                if gw not in self.gateway_sockets:
                    gateway_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.gateway_sockets[gw] = gateway_sock
                    gw_IP, gw_port = gw.split(':')
                    gateway_sock.connect((gw_IP, int(gw_port)))

                json_output_str = json.dumps(output)
                #print (f"{self.description} sending output --> {json_output_str}")
                sock_util.send_msg(self.gateway_sockets[gw], json_output_str)

        # OUTPUT of NAVAL_MINE_DETECTION_SERVICE
        # Destination: UI
        # Action: Trigger CounterService if Mine detected
        elif service_id == "sonar_svc_1":
        #elif service_name == "Sonar":
            json_output_str = json.dumps(output)
            #print (f"[POS] receiving output --> {json_output_str}")
            self.RBMQ.send("", self.description + "_" + service_id, json_output_str)

            if output["content"] == "Mine":
                # Fetch service_id of COUNTER_SERVICE
                self.RBMQ.send("", self.description + "_counter_svc_1", "Mine")

        # OUTPUT of FLOWER_ANALYSIS_SERVICE
        # Destination: UI
        elif service_id == "flower_svc_1":
        #elif service_name == "Iris":
            json_output_str = json.dumps(output)
            #print (f"[POS] receiving output --> {json_output_str}")
            self.RBMQ.send("", self.description + "_" + service_id, json_output_str)
            
        elif service_id == "earthquake_svc_1":
        #elif service_id == "Earthquake_Service":
            json_output_str = json.dumps(output)
            print (f"[POS] receiving output --> {json_output_str}")
            self.RBMQ.send("", self.description + "_" + service_id, json_output_str)
        else:
            print ("[POS] It shouldn't reach here, service_id: ", service_id)


    # function to listen to output data from the services
    # route the data to the destinations according to configuration
    def init_output_stream(self):
        self.RBMQ.receive(self.handle_service_output, '', self.SERVICE_OUTPUT_QUEUE)
    
    # SERVICE APIs

    def service_output_send(self, service_id, content):
        output = {}
        output["service_id"] = service_id
        output["content"] = content
        json_output_str = json.dumps(output)
        self.RBMQ.send("", self.SERVICE_OUTPUT_QUEUE, json_output_str)


if __name__ == "__main__":
    platform_output_stream = PlatformOutputStream()
    threading.Thread(target = platform_output_stream.init_output_stream).start()
