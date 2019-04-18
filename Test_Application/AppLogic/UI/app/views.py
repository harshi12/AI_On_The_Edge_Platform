import sys
from pathlib import Path
home = str(Path.home())
path = home+'/Platform/'
sys.path.insert (0, path)
from queue_req_resp import *
from app import app
import json
from flask import Flask,render_template,request,redirect, url_for
from threading import Thread
from googleapiclient.discovery import build
from oauth2client import client, tools, file
from googleapiclient.http import MediaFileUpload
from run import foo

SCOPES = 'https://www.googleapis.com/auth/drive'

@app.route('/')
def firstpage():
    return render_template('p.html',title = 'IAS')

@app.route('/startservice' ,methods = ['GET','POST'] )
def startservice():
    if request.method == "GET":
        service_name = request.args.get('sname')
        print(service_name)
    return(json.dumps(""))

@app.route('/redirect_link')
def reroute():
	print("came here")
	return redirect('http://google.com/', code = 302)

@app.route('/stopservice' ,methods = ['GET','POST'] )
def stopservice():
    print("Stop Service")
    if request.method == "GET":
        service_name=request.args.get('sname')
        print(service_name)
    return(json.dumps(""))

