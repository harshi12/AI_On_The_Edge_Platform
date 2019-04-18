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
import socket
import Socket.utilities as sock_util

inputQueue = "PlatformOutputStream_" + str(foo)
SCOPES = 'https://www.googleapis.com/auth/drive'
RMQ = RabbitMQ()
setosa = 0
virginica = 0
versicolor = 0

def receive_input_from_socket():
    service_gateway_output_listen = socket.socket()
    service_gateway_output_listen.bind(('', 5004))
    service_gateway_output_listen.listen(15)
    while True: 
        service_socket,addr = service_gateway_output_listen.accept()
        data = sock_util.recv_msg(service_socket)
        callback(None,None,None, data)   

def receiveInput(exchange, key):
    RMQ.receive(callback, exchange, key)

def callback(ch, method, properties, body):
    global setosa
    global versicolor
    global virginica

    if not isinstance(body, str):
            body = body.decode()

    body = json.loads(body)
    body = body["content"]

    if(body == "Iris-Setosa"):
        setosa += 1
    elif(body == "Iris-Virginica"):
        virginica += 1
    elif(body == "Iris-Versicolor"):
        versicolor += 1
    else:
        pass
    
    print("Setosa : ", setosa, "Versicolor : ", versicolor, "Virginica : ", virginica)

t1 = Thread(target = receiveInput, args = ('', inputQueue)) #thread that will monitor HM_SM Queue	
t1.start()
t2 = Thread(target = receive_input_from_socket) #thread that will monitor HM_SM Queue	
t2.start()

@app.route('/')
def firstpage():
    return render_template('p.html',title='IAS')

@app.route('/load_graph')
def load_graph():
    '''
        When called, this function will receive data from some stream and send it back to the caller
    '''
    global setosa
    global versicolor
    global virginica

    freq_list = [setosa, versicolor, virginica]
    freq_list = {"list" : freq_list}
    data = json.dumps(freq_list)
    return data