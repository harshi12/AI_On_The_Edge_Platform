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

def response_send(response,sname):
    res = {}
    sname
    res["response"] = response
    json_resp = json.dumps(res)

    print ("Sent Response: {json_resp}")
    RBMQ.send("", "DB_"+sname, json_resp)

def db_server_requests_cb(ch, method, properties, body):
    req = json.loads(body)
    resp = {}
    if req["opcode"] == "SERVICE_ID_GET":
        print (f"Received Request: {req}")
        responses = Service.query.filter(Service.service_name==req["service_name"]).all()
        for response in responses:
            sid = response.service_id
            resp["service_name"]=sid
        # gw_id = response.gw_id
        # print(gw_id)
        response_send(resp,req["service_name"])


def handle_db_client_requests(exchange, queue_name):
    print ("DB Server receiving requests!!")
    while True:
        print("Queue Name: ", queue_name)

        RBMQ.receive(db_server_requests_cb, exchange,"modules_DB")
