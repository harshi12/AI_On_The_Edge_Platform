import requests
import sys
import zipfile
import json
import os
import time
from queue_req_resp import RabbitMQ
from app.models import Gateway,Person,Application,User,Sensor
DB_REQUEST_QUEUE = "modules_DB"

# RBMQ = RabbitMQ()
class DATABASE_SERVER:
    def __init__(self,DB_REQUEST_QUEUE = "modules_DB"):
        self.DB_REQUEST_QUEUE = DB_REQUEST_QUEUE

    def response_send(module, response):
        res = {}
        res["response"] = response
        json_resp = json.dumps(res)
        print (f"Sent Response: {json_resp}")
        RBMQ.send("", "DB_"+module, json_resp)

    def db_server_requests_cb(ch, method, properties, body):
        req = json.loads(body)
        resp = {}
        if req["opcode"] == "GATEWAYS_AT_LOC_GET":
            location = req["location"]
            print (f"Received Request: {req}")
            responses = Gateway.query.filter(Gateway.gw_location== location).all()
            for response in responses:
                id = response.gw_id
                ip = response.gw_IP
                port = response.gw_port
                addr  = ip+":"+port
                resp[id]=addr
            response_send(req["module"], resp)
        elif req["opcode"] == "SENSORS_AT_GATEWAY_GET":
            gateway_id = req["gateway_id"]
            responses = Sensor.query.filter(Sensor.connected_gw_id== gateway_id).all()
            for response in responses:
                id = response.sensor_id
                type = response.sensor_type
                resp[id]=type
            response_send(req["module"],resp)
        elif req["opcode"] == "APPLICATION_DATA_LOC_GET":
            app_id = req["app_id"]
            responses = Application.query.filter(Application.app_id==app_id).all()
            for response in responses:
                app_logic_loc = response.app_logic_loc
                config_file_loc = response.config_file_loc
                model_loc = response.model_loc
                links = app_logic_loc+"|"+config_file_loc+"|"+model_loc
                resp[app_id] = links
            response_send(req["module"],resp)

    def handle_db_client_requests(exchange, queue_name):
        print ("DB Server receiving requests!!")
        while True:
            RBMQ.receive(db_server_requests_cb, exchange, queue_name)
