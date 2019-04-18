import sys
from pathlib import Path
home = str(Path.home())
path = home+'/Platform/'
sys.path.insert (0, path)
from queue_req_resp import *
from app import app
import pika
import json
import pandas as pd
from flask import Flask,render_template,request,redirect
import numpy as np
from googleapiclient.discovery import build
from oauth2client import client, tools, file
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from threading import Thread
from run import foo

SCOPES = 'https://www.googleapis.com/auth/drive'
RMQ = RabbitMQ()
data = ""
signal = ""
inputQueue = "PlatformOutputStream_" + str(foo)

def receiveInput(exchange, key):
    RMQ.receive(callback, exchange, key)

def callback(ch, method, properties, body):
    global data
    global signal
    if not isinstance(body, str):
            body = body.decode()
    body = json.loads(body)
    data = body["content"]
    if data.lower() == "mine":
        signal = "red"
    elif data.lower() == "rock":
        signal = "green"
    print("callback : ", data)

t1 = Thread(target = receiveInput, args = ('', inputQueue))
t1.start()

@app.route('/')
def firstpage():
    return render_template('p.html',title='IAS')


@app.route('/sonar_status')
def status():
    '''
        When called, this function will receive data from some stream and send it back to the caller
    '''
    global signal
    status = {"status" : signal}
    status = json.dumps(status)
    print(status)
    return status