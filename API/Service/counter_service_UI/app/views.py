import sys
sys.path.insert (0, '../../')
sys.path.insert (0, '../../../')
from RabbitMQ.message_queue import *
from app import app
import json
from flask import Flask,render_template,request,redirect
from threading import Thread
from googleapiclient.discovery import build
from oauth2client import client, tools, file
from googleapiclient.http import MediaFileUpload
from run import foo

SCOPES = 'https://www.googleapis.com/auth/drive'
RMQ = RabbitMQ()
count = 0
inputQueue = "PlatformOutputStream_" + str(foo)

def receiveInput(exchange, key):
	RMQ.receive(callback, exchange, key)

def callback(ch, method, properties, body):
	global count
	if not isinstance(body, str):
		body = body.decode()
	count = int(body)

t1 = Thread(target = receiveInput, args = ('', inputQueue))
t1.start()

@app.route('/')
def firstpage():
    return render_template('p.html',title='Counter Service UI')

@app.route('/counter')
def getCount():
	''' When called, this function will receive data from some stream and send it back to the caller '''
	global count
	data = {"count" : count}
	data = json.dumps(data)
	return data