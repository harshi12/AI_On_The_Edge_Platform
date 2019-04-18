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
from db_client import *
from Registry.Registry_API import Registry_API
RBMQ = RabbitMQ()
RAPI = Registry_API()
dc = DATABASE_CLIENT()
# from googleapiclient.discovery import build
# from oauth2client import client, tools, file
# from googleapiclient.http import MediaFileUpload
service_id = None
# SCOPES = 'https://www.googleapis.com/auth/drive'

@app.route('/')
def firstpage():
    return render_template('p.html',title = 'IAS')

@app.route('/startservice' ,methods = ['GET','POST'] )
def startservice():
    global service_id
    if request.method == "GET":
        service_name = request.args.get('sname')
        print(service_name)
        resp=dc.db_service_id_get(service_name)
        service_id = resp[service_name]
        request_MT = {"Request_Type": "Service_Submit","Service_ID" : service_id,"Instances" : 1}
        RBMQ.send("","FM_HM",request_MT)
    return(json.dumps(""))

@app.route('/redirect_link')
def reroute():
    global service_id
    l = [service_id]
    RAPI.Read_Service_Inst_info(l,"FMSI_RG","RG_FMSI")
    service_info = RBMQ.receive_nonblock("","RG_FMSI")
    for service_id in service_info:
        info = service_info[service_id]
        ip = info[0][0]
        port = info[0][1]
        url = "http://"+ip+":"+port
    return redirect(url,code=302)

@app.route('/stopservice' ,methods = ['GET','POST'] )
def stopservice():
    global service_id
    if request.method == "GET":
        service_name=request.args.get('sname')
        print(service_name)
        resp=dc.db_sensors_get(service_name)
        service_id = resp[service_name]
        l = [service_id]
        RAPI.Read_Service_Inst_info(l,"FMSI_RG","RG_FMSI")
        service_info = RBMQ.receive_nonblock("","RG_FMSI")
        for service_id in service_info:
            info = service_info[service_id]
            ip = info[0][0]
            process_id = info[0][3]
            instance_id = info[0][5]
            request_MT = {"Request_Type": "Kill","IP" : ip,"PID" : process_id,"Service_ID" : service_id,"Instance_ID":instance_id}
            RBMQ.send("","modules_SM",request_MT)
    return(json.dumps(""))
