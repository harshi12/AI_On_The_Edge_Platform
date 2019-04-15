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
import time

SCOPES = 'https://www.googleapis.com/auth/drive'

@app.route('/')
def firstpage():
    return render_template('p.html',title='Counter Service UI')

@app.route('/counter')
def getCount():
    '''
        When called, this function will receive data from some stream and send it back to the caller
		# TODO : Implement the input stream listener        
    '''
    getCount.count += 1
    data = {"count" : getCount.count}
    data = json.dumps(data)
    return data
getCount.count = 0