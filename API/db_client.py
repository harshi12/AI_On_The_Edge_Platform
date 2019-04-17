import requests
import sys
import json
import os
import time
from queue_req_resp import RabbitMQ

# RBMQ = RabbitMQ()
class DATABASE_CLIENT:
    def __init__(self,DB_REQUEST_QUEUE = "modules_DB"):
        self.DB_REQUEST_QUEUE = DB_REQUEST_QUEUE

    def db_gateways_get(module, location):
        req = {}
        req["module"] = module
        req["opcode"] = "GATEWAYS_AT_LOC_GET"
        req["location"] = location
        json_req = json.dumps(req)
        RBMQ.send("", DB_REQUEST_QUEUE, json_req)
        print (f"Sent Request: {json_req}")
        resp = RBMQ.receive_nonblock("", "DB_"+module)
        print (f"Received Response: {resp}")
        return resp

        
    def db_sensors_get(module,gateway_id):
        req = {}
        req["module"] = module
        req["opcode"] = "SENSORS_AT_GATEWAY_GET"
        req["gateway_id"] = gateway_id
        json_req = json.dumps(req)
        RBMQ.send("", DB_REQUEST_QUEUE, json_req)
        resp = RBMQ.receive_nonblock("", "DB_"+module)
        return resp

    def db_app_links_get(module,app_id):
        req = {}
        req["module"] = module
        req["opcode"] = "APPLICATION_DATA_LOC_GET"
        req["app_id"] = app_id
        json_req = json.dumps(req)
        RBMQ.send("", DB_REQUEST_QUEUE, json_req)
        resp = RBMQ.receive_nonblock("", "DB_"+module)
        return resp
