from app import app
import pika
import json
import pandas as pd
from flask import Flask,render_template,request,redirect
from threading import Thread
import numpy as np
from googleapiclient.discovery import build
from oauth2client import client, tools, file
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
SCOPES = 'https://www.googleapis.com/auth/drive'

@app.route('/')
def firstpage():
    return render_template('p.html',title='IAS')

@app.route('/load_graph')
def load_graph():
    '''
        When called, this function will receive data from some stream and send it back to the caller
    '''
    val_list = np.random.randint(20, 100, (1,3))
    val_list1 = val_list.tolist()
    data = {"values" : val_list1}
    data = json.dumps(data)
    return data