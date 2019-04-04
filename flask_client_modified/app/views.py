from app import app

#shared queue for communication between gateways and service manager and other such scenarios

import pika
import json
import pandas as pd
from flask import Flask,render_template,request,redirect
from threading import Thread
import numpy as np
BATCH_COUNT = 10
class RabbitMQ:
    def __init__(self):
    	self.server_IP = "192.168.43.135"
    	self.server_Port = 5672
    	self.credentials = pika.PlainCredentials("harshita","123")
    	self.create_queue("", "AD_SM")
    	self.create_ServiceQueues("SM","Docker")
    	self.create_ServiceQueues("SM", "Scheduler")

    def create_queue(self, exchange_name, queue_name):
    	channel, conn = self.create_connection()
    	# channel.exchange_declare(exchange='', exchange_type='direct')
    	channel.queue_declare(queue = queue_name, durable = True)
    	# channel.queue_bind(exchange=exchange_name, queue=queue_name)
    	conn.close()

    def create_ServiceQueues(self,Module1, Module2):
    	self.create_queue("", str(Module1+"_"+Module2))
    	self.create_queue("", str(Module2+"_"+Module1))

    def create_connection(self):
    	connection = pika.BlockingConnection(pika.ConnectionParameters(self.server_IP, self.server_Port, '/', self.credentials))
    	channel = connection.channel()
    	return channel, connection

    def send(self,exchange_name, queue_name, message):
    	channel, conn = self.create_connection()
    	self.create_queue(exchange_name, queue_name)
    	channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    	# print(" [x] Sent",message)
    	conn.close()

    def receive(self, callback, exchange_name, queue_name):
        channel, conn = self.create_connection()
        self.create_queue(exchange_name, queue_name)

    	# def callback(ch, method, properties, body):
    	#     print(" [x] Received %r" % body)
    	# 	process(body)

        channel.basic_consume(callback, queue = queue_name, no_ack = True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def receive_nonblock(self, exchange_name, queue_name):
        channel, conn = self.create_connection()
        self.create_queue(exchange_name, queue_name)
        method_frame, header_frame, body = channel.basic_get(queue_name, True)
        # body = channel.basic_get(queue_name, True) #callback, queue = queue_name, no_ack = True)
        # print("In queue:", type(body))
        return body

# print(os.getcwd())
# # os.

# from a import uploadmodel,uploadconfig
# from queue_req_resp import RabbitMQ



@app.route('/')
def firstpage():
    return render_template('p.html',title='IAS')

@app.route('/2',methods=['GET','POST'])
def Uploaded():
    if request.method == "GET":
        filepath = request.args.get("filepath")
        modelname = request.args.get("modelname")
        # configpath = request.args.get("configpath")
        # configname = request.args.get("configname")
        modelid = uploadmodel(filepath,modelname)
        # configid = uploadconfig(configpath,configname)
        send_to_service_manager(modelid)
        return render_template('q.html',title='IAS 2')

@app.route('/3',methods=['GET','POST'])
def data_send():
    if request.method == "GET":
        test_file = request.args.get("testfile")
        test_df = pd.read_csv(test_file)
#generate json
        eval_data = test_df[test_df.columns[0:60]].values
        for i in range(BATCH_COUNT):
            json_str = json.dumps(str({"request_type": "input_data","data" : eval_data[i*10:(i+1)*10].tolist()}))
            #sending to queue
            obj = RabbitMQ()
            obj.send("","Model1_Input",json_str)
        return redirect('/5')

def output_recv(ch,method,properties,body):
    body = body.decode()
    data = json.loads(body)
    predictions = data["predictions"]
    predictions = np.array(predictions)
    predictions = np.argmax(predictions,axis=1)
    print("#################################################################################################")
    # print("Output for Batch ",count)
    print(predictions)

def receive_model1_output(exchange,key):
    obj = RabbitMQ()
    obj.receive(output_recv,exchange,key)


@app.route('/5')
def test_data():
    t1 = Thread(target = receive_model1_output, args = ('', "Model1_Output"))
    t1.start()
    return redirect('/')

    # count = 0
    # while count<BATCH_COUNT:
    #     # obj.receive(output_recv, "", "Model1_Output")
    #     body = obj.receive_nonblock("", "Model1_Output")
    #     if(body == None):
    #         pass
    #     else:
    #         count += 1
    #         body = body.decode()
    #         data = json.loads(body)
    #         predictions = data["predictions"]
    #         predictions = np.array(predictions)
    #         predictions = np.argmax(predictions,axis=1)
    #         print("#################################################################################################")
    #         print("Output for Batch ",count)
    #         print(predictions)
    #     # render_template("5.html",predictions=predictions)
    # return redirect('/')
    # data = ast.literal_eval(data)


from googleapiclient.discovery import build
from oauth2client import client, tools, file
from googleapiclient.http import MediaFileUpload
# from queue_req_resp import RabbitMQ
from httplib2 import Http
import json

SCOPES = 'https://www.googleapis.com/auth/drive'

def uploadmodel(filepath,modelname):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    drive_service = build('drive', 'v3', http=creds.authorize(Http()))

    folder_id = '1c63s9RQ_xrb58BGXhyvWQnJEasfc0Vgn'
    file_metadata = { 'name':modelname,'parents': [folder_id]}
    media = MediaFileUpload(filepath, mimetype='application/zip', resumable=True)
    DATA = drive_service.files().create(body=file_metadata,media_body=media,fields='id').execute()
    did = DATA.get('id')
    return did

# def uploadconfig(configpath,configname):
#     store = file.Storage('token.json')
#     creds = store.get()
#     if not creds or creds.invalid:
#         flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
#         creds = tools.run_flow(flow, store)
#     drive_service = build('drive', 'v3', http=creds.authorize(Http()))
#
#     folder_id = '1c63s9RQ_xrb58BGXhyvWQnJEasfc0Vgn'
#     file_metadata = { 'name':configname,'parents': [folder_id]}
#     media = MediaFileUpload(filepath, mimetype='application/vnd.google-apps.script+json', resumable=True)
#     DATA = drive_service.files().create(body=file_metadata,media_body=media,fields='id').execute()
#     did = DATA.get('id')
#     return did

def send_to_service_manager(modelid):
    request_packet = json.dumps({"request_type":"serve_model","model":modelid})
    # request_packet = json.dumps({"request_type":"serve_model","model":modelid,"config_file":configid})
    request_packet_s = str(request_packet)
    obj = RabbitMQ()
    obj.send("","AD_SM",request_packet)
