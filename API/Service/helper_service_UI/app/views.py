import sys
sys.path.insert (0, '../../')
sys.path.insert (0, '../../../')

from app import app
import pika
from RabbitMQ.message_queue import *
import json
import pandas as pd
from flask import Flask,render_template,request,redirect
import numpy as np
from googleapiclient.discovery import build
from oauth2client import client, tools, file
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from threading import Thread

SCOPES = 'https://www.googleapis.com/auth/drive'
RMQ = RabbitMQ()
setosa = 0
virginica = 0
versicolor = 0

@app.route('/')
def firstpage():
    t1 = Thread(target = receiveInput, args = ('', "helper_test")) #thread that will monitor HM_SM Queue	
    t1.start()
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

def receiveInput(exchange, key):
    RMQ.receive(callback, exchange, key)

def callback(ch, method, properties, body):
    global setosa
    global versicolor
    global virginica

    if not isinstance(body, str):
            body = body.decode()

    if(body == "Iris-Setosa"):
        setosa += 1
    elif(body == "Iris-Virginica"):
        virginica += 1
    elif(body == "Iris-Versicolor"):
        versicolor += 1
    else:
        pass
    
    print("Setosa : ", setosa, "Versicolor : ", versicolor, "Virginica : ", virginica)
