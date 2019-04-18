import requests
import sys
import zipfile
import json
import os
import time
# import app
from queue_req_resp import RabbitMQ
from threading import Thread
from app import db
from app.models import Gateway
DB_REQUEST_QUEUE = "modules_DB"

RBMQ = RabbitMQ()

def response_send(module, response):
    res = {}
    res["response"] = response
    json_resp = json.dumps(res)

    print ("Sent Response: {json_resp}")
    RBMQ.send("", "DB_"+module, json_resp)

def db_server_requests_cb(ch, method, properties, body):
    req = json.loads(body)
    resp = {}
    if req["opcode"] == "GATEWAYS_AT_LOC_GET":
        print (f"Received Request: {req}")
        responses = Gateway.query.filter(Gateway.gw_location=='IIIT').all()
        for response in responses:
            id = response.gw_id
            ip = response.gw_IP
            port = response.gw_port
            addr  = ip+":"+port
            resp[id]=addr
        # gw_id = response.gw_id
        # print(gw_id)
        response_send(req["module"], resp)

def handle_db_client_requests(exchange, queue_name):
    print ("DB Server receiving requests!!")
    while True:
        print("Queue Name: ", queue_name)

        RBMQ.receive(db_server_requests_cb, exchange, queue_name)
