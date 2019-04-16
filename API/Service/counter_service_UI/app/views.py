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

SCOPES = 'https://www.googleapis.com/auth/drive'
RMQ = RabbitMQ()
count = 0
@app.route('/')
def firstpage():
	# TODO : Insert proper queuename in next line
    t1 = Thread(target = receiveInput, args = ('', "temp")) #thread that will monitor HM_SM Queue	
    t1.start()
    return render_template('p.html',title='Counter Service UI')

def receiveInput(exchange, key):
	RMQ.receive(callback, exchange, key)

def callback(ch, method, properties, body):
	global count
	if not isinstance(body, str):
		body = body.decode()
	count = int(body)

@app.route('/counter')
def getCount():
	''' When called, this function will receive data from some stream and send it back to the caller '''
	global count
	data = {"count" : count}
	data = json.dumps(data)
	return data