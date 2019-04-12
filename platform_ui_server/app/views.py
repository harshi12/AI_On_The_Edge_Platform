from app import app

#shared queue for communication between gateways and service manager and other such scenarios

import pika
import json
import pandas as pd
from flask import Flask,render_template, url_for
from flask import request, redirect, session , logging , flash
from functools import wraps
from threading import Thread
from app import db,bcrypt
from passlib.hash import sha256_crypt
from sqlalchemy import create_engine , update
from app.models import Person,Application,User,Gateway,Sensor
import numpy as np
import os
from app.Deployment_Manager import Deploy
from db_server import *

from werkzeug.utils import secure_filename

BATCH_COUNT = 10

APP_UPLOAD_FOLDER = '/home/bhavidhingra/google-drive-iiith/Semester_#2/CSE563_Internals_of_Application_Servers/Hackathon/self_after_3/platform_ui_server1/Downloads/Applications/'

GW_UPLOAD_FOLDER = '/home/bhavidhingra/google-drive-iiith/Semester_#2/CSE563_Internals_of_Application_Servers/Hackathon/self_after_3/platform_ui_server1/Downloads/Gateways/'

#app = Flask(__name__)
app.config['APP_UPLOAD_FOLDER'] = APP_UPLOAD_FOLDER
app.config['GW_UPLOAD_FOLDER'] = GW_UPLOAD_FOLDER

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

    messages=[]

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        #process(body)
        messages.append(body)

    def receive(self, callback, exchange_name, queue_name):
        channel, conn = self.create_connection()
        self.create_queue(exchange_name, queue_name)
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

# Check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			# flash('Unauthorized, Please login', 'danger')
			return redirect(url_for('login'))
	return wrap

# @login_manager.user_loader
# def load_user(user_id):
#     return None

def db_init():
    if not db_init.is_initialized:
        t1 = Thread(target =handle_db_client_requests, args = ('', "modules_DB",))
        t1.start()
        db_init.is_initialized = True

db_init.is_initialized = False

@app.route('/')
@app.route('/index')
def index():
    # load_db()
    db_init()
    if 'logged_in' in session:
        return redirect(url_for('home'))
    return render_template('login.html',title='IAS')


def load_db():
    #app_dev=App_Dev(AD_name="Team2",password="1729")
    #app_1 = Application( app_name = "Sonar" , app_desc="Determine Mines or Rocks using Sonar" , AD_id = 1 , app_logic_loc="NULL" , config_file_loc = "NULL" , model_loc = "NULL" , app_ui_server = "NULL")
    # gw_1=Gateway( gw_name="gw1" , gw_location="IIIT" , gw_IP = "NULL" , gw_port=0)
    # gw_2=Gateway( gw_name="gw2" , gw_location="Hitech City" , gw_IP = "NULL" , gw_port=0)
    # sensor_1_1 = Sensor( sensor_type="A" , sensor_location = "IIIT" , connected_gw_id=1 )
    # sensor_1_2 = Sensor( sensor_type="B" , sensor_location = "IIIT" , connected_gw_id=1 )
    # sensor_1_3 = Sensor( sensor_type="C" , sensor_location = "IIIT" , connected_gw_id=1 )
    # sensor_2_1 = Sensor( sensor_type="A" , sensor_location = "Hitech City" , connected_gw_id=2 )
    # sensor_2_2 = Sensor( sensor_type="A" , sensor_location = "Hitech City" , connected_gw_id=2 )
    #db.session.add(app_dev)
    #db.session.add(app_1)
    # db.session.add(gw_1)
    # db.session.add(gw_2)
    # db.session.add(sensor_1_1)
    # db.session.add(sensor_1_2)
    # db.session.add(sensor_1_3)
    # db.session.add(sensor_2_1)
    # db.session.add(sensor_2_1)
    # db.session.commit()
    return 


@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # name = form.name.data
        username = None
        password = None
        username = request.form['username']

        password = request.form['password']

        if( username == None or password == None ):
            flash('Please enter all details', 'danger')
            return redirect(url_for('register'))

        # username = form.username.data
        category = request.form['category']

        # print (str(request.form['password']))
        # print (str(request.form['confirm_password']))

        # check entered passwords
        password = sha256_crypt.encrypt(request.form['password'])
        # password_candidate = request.form['password']
        confirm_password = request.form['confirm_password']

        person=None
        if category == "user":
        	# person = User.query.filter_by(username=username).first()
            person_type = 1
        elif category == "app_dev":
        	# person = Application.query.filter_by(username=username).first()
            person_type = 2
        elif category == "nw_admin":
            # person = Application.query.filter_by(username=username).first()
            person_type = 3

        # if person is None:
        # 	flash('Username doesn\'t exist!!', 'danger')
        # 	return redirect(url_for('register'))

        if not sha256_crypt.verify(confirm_password, password):
        	flash('Passwords do not match!!', 'danger')
        	return redirect(url_for('register'))

        password = password

        person = Person(username=username , password=password , person_type = person_type)
        db.session.add(person)
        db.session.commit()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')



@app.route('/login',methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        category = request.form['category']

        user = None
        app_dev = None
        nw_admin = None

        if category == "user":
            user = Person.query.filter_by(username=username).first()

            if user is None:
                error = 'Entry not found'
                return render_template('login.html', error=error)

            password = user.password
            username = user.username
            per_type = user.person_type
        elif category == "app_dev":
            app_dev = Person.query.filter_by(username=username).first()

            if app_dev is None:
                error = 'Entry not found'
                return render_template('login.html', error=error)

            password = app_dev.password
            username = app_dev.username
            per_type = app_dev.person_type
            print("**********",password)
        else:
            print("Network Admin")
            nw_admin = Person.query.filter_by(username=username).first()

            if nw_admin is None:
                error = 'Entry not found'
                return render_template('login.html', error=error)

            password = nw_admin.password
            username = nw_admin.username
            per_type = nw_admin.person_type

            print("**********",password)

        if user is not None or app_dev is not None or nw_admin is not None:

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['person_type'] = per_type
                if per_type == 1:
                    session['user_id'] = user.person_id
                elif per_type == 2:
                    session['app_dev_id'] = app_dev.person_id
                else:
                    session['nw_admin_id'] = nw_admin.person_id

                return redirect(url_for('home'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            error = 'Entry not found'
            return render_template('login.html', error=error)
    return render_template('login.html')


# Logout
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('index'))


#Home
@app.route('/home')
@is_logged_in
def home():
    if session['person_type'] == 1:
       return redirect(url_for('run_application'))
    elif session['person_type'] == 2:
        return redirect(url_for('add_application'))
    else:
        return redirect(url_for('register_gw'))
    
@app.route('/run_app')
@is_logged_in
def run_application():
    if session['person_type'] == 1:
        return render_template('run_app.html',title='IAS')
    return redirect(url_for('index'))

@app.route('/add_app')
@is_logged_in
def add_application():
    if session['person_type'] == 2:
        return render_template('add_app.html',title="IAS 1")
    return redirect(url_for('index'))


@app.route('/register_gw')
def register_gw():
    if session['person_type'] == 3:
        return render_template('register_gw.html',title="IAS3")
    return redirect(url_for('index'))


#Run App
@app.route('/redirect_app',methods=['GET', 'POST'])
def redirect_app():
    app_name= request.form["applications"]
    print(app_name)
    #TODO: Read app_id,app_ui_server from DB using app_name 
    app_id=145
    app_ui_server = "192.168.31.34:5001"
    url= "http://" + app_ui_server + "/" +str(app_id)
    return redirect(url,code=302)

#Add App
@app.route('/upload_app',methods=['GET','POST'])
def upload_app():
    if request.method == "POST":
        # filepath = request.args.get("filepath")
        appname = request.form["appname"]
        print(appname)
        appfile = request.files['appfile']
        if appfile.filename == '':
            flash('No selected file')
            return render_template('p.html',title="IAS 1")
        #modelid = uploadmodel(filepath,modelname)
        # configid = uploadconfig(configpath,configname)
        #send_to_service_manager(modelid)
        file_list=appfile.filename.split(".")
        print(file_list)
        if '.' in appfile.filename and file_list[1] == "zip":
            filename = secure_filename(appfile.filename)
            appfile.save(os.path.join(app.config['APP_UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file', filename=filename))
            deploy_file(filename)
            return render_template('uploaded.html')
        else:
            flash('Upload .zip file')
            return render_template('p.html',title="IAS 1")

def deploy_file(filename):
    #TODO: Do Deployment
    app_name =filename
    AD_id = session['app_dev_id']

    app = Application( app_name = app_name ,  AD_id = AD_id , app_logic_loc="EMPTY" , config_file_loc = "EMPTY" , model_loc = "EMPTY" , app_ui_server = "EMPTY")
    db.session.add(app)
    db.session.commit()

    app=Application.query.filter_by(app_name=app_name).first()
    app_id = app.app_id

    App_path = APP_UPLOAD_FOLDER+filename

    Model_Link , App_Link , Config_Link = Deploy(AD_id,app_id,App_path)

    # Application.query.filter_by(app_id=app_id).first().update({app_logic_loc : App_Link , config_file_loc : Config_Link , model_loc : Model_Link } , synchronize_session = False)
    app.app_logic_loc = App_Link
    app.config_file_loc = Config_Link
    app.model_loc = Model_Link
    db.session.add(app)
    db.session.commit()

    print("File uploaded")

#Register Gateway
@app.route('/add_gw',methods=['GET','POST'])
def add_gw():
    if request.method == "POST":
        # filepath = request.args.get("filepath")
        gwname = request.form["gwname"]
        print(gwname)
        gwfile = request.files['gwfile']
        if gwfile.filename == '':
            flash('No selected file')
            return render_template('register_gw.html',title="IAS 1")
        #modelid = uploadmodel(filepath,modelname)
        # configid = uploadconfig(configpath,configname)
        #send_to_service_manager(modelid)
        file_list=gwfile.filename.split(".")
        print(file_list)
        if '.' in gwfile.filename and file_list[1] == "json":
            filename = secure_filename(gwfile.filename)
            gwfile.save(os.path.join(app.config['GW_UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file', filename=filename))
            gw_parse_n_save(filename)
            #TODO: Delete Config file ??
            return render_template('uploaded.html')
        else:
            flash('Upload config in .json format')
            return render_template('register_gw.html',title="IAS 1")
    return render_template('register_gw.html',title="IAS 1")


def gw_parse_n_save(filename):
    #Parsing
    #config_filename = filename
    config_file_path = GW_UPLOAD_FOLDER+filename

    print(config_file_path)

    with open(config_file_path) as f:
        data = json.load(f)

    gw_name = data["gw_name"]
    gw_location = data["gw_location"]
    gw_IP = data["gw_address"]["IP"]
    gw_port = data["gw_address"]["port"]
    #DB
    gw=Gateway( gw_name=gw_name , gw_location=gw_location , gw_IP = gw_IP , gw_port=gw_port)
    db.session.add(gw)
    db.session.commit()

    gw = Gateway.query.filter_by(gw_name=gw_name).first()
    gw_id = gw.gw_id

    sensor_types = []
    for s in data["sensors"]:
        #sensor_types.append(s["type"])
        sensor_type = s["type"]
        #DB
        sensor = Sensor ( sensor_type=sensor_type , connected_gw_id=gw_id)
        db.session.add(sensor)
    db.session.commit()

    print("Saved in Database")
    return


# @app.route('/3',methods=['GET','POST'])
# def data_send():
#     if request.method == "GET":
#         test_file = request.args.get("testfile")
#         test_df = pd.read_csv(test_file)
# #generate json
#         eval_data = test_df[test_df.columns[0:60]].values
#         for i in range(BATCH_COUNT):
#             json_str = json.dumps(str({"request_type": "input_data","data" : eval_data[i*10:(i+1)*10].tolist()}))
#             #sending to queue
#             obj = RabbitMQ()
#             obj.send("","Model1_Input",json_str)
#         return redirect('/5')

# def output_recv(ch,method,properties,body):
#     body = body.decode()
#     data = json.loads(body)
#     predictions = data["predictions"]
#     predictions = np.array(predictions)
#     predictions = np.argmax(predictions,axis=1)
#     print("#################################################################################################")
#     # print("Output for Batch ",count)
#     print(predictions)

# def receive_model1_output(exchange,key):
#     obj = RabbitMQ()
#     obj.receive(output_recv,exchange,key)


# @app.route('/5')
# def test_data():
#     t1 = Thread(target = receive_model1_output, args = ('', "Model1_Output"))
#     t1.start()
#     return redirect('/')

#     # count = 0
#     # while count<BATCH_COUNT:
#     #     # obj.receive(output_recv, "", "Model1_Output")
#     #     body = obj.receive_nonblock("", "Model1_Output")
#     #     if(body == None):
#     #         pass
#     #     else:
#     #         count += 1
#     #         body = body.decode()
#     #         data = json.loads(body)
#     #         predictions = data["predictions"]
#     #         predictions = np.array(predictions)
#     #         predictions = np.argmax(predictions,axis=1)
#     #         print("#################################################################################################")
#     #         print("Output for Batch ",count)
#     #         print(predictions)
#     #     # render_template("5.html",predictions=predictions)
#     # return redirect('/')
#     # data = ast.literal_eval(data)


# # from googleapiclient.discovery import build
# # from oauth2client import client, tools, file
# # from googleapiclient.http import MediaFileUpload
# # # from queue_req_resp import RabbitMQ
# # from httplib2 import Http
# import json

# # SCOPES = 'https://www.googleapis.com/auth/drive'

# # def uploadmodel(filepath,modelname):
# #     store = file.Storage('token.json')
# #     creds = store.get()
# #     if not creds or creds.invalid:
# #         flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
# #         creds = tools.run_flow(flow, store)
# #     drive_service = build('drive', 'v3', http=creds.authorize(Http()))

# #     folder_id = '1c63s9RQ_xrb58BGXhyvWQnJEasfc0Vgn'
# #     file_metadata = { 'name':modelname,'parents': [folder_id]}
# #     media = MediaFileUpload(filepath, mimetype='application/zip', resumable=True)
# #     DATA = drive_service.files().create(body=file_metadata,media_body=media,fields='id').execute()
# #     did = DATA.get('id')
# #     return did

# # def uploadconfig(configpath,configname):
# #     store = file.Storage('token.json')
# #     creds = store.get()
# #     if not creds or creds.invalid:
# #         flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
# #         creds = tools.run_flow(flow, store)
# #     drive_service = build('drive', 'v3', http=creds.authorize(Http()))
# #
# #     folder_id = '1c63s9RQ_xrb58BGXhyvWQnJEasfc0Vgn'
# #     file_metadata = { 'name':configname,'parents': [folder_id]}
# #     media = MediaFileUpload(filepath, mimetype='application/vnd.google-apps.script+json', resumable=True)
# #     DATA = drive_service.files().create(body=file_metadata,media_body=media,fields='id').execute()
# #     did = DATA.get('id')
# #     return did

# def send_to_service_manager(modelid):
#     request_packet = json.dumps({"request_type":"serve_model","model":modelid})
#     # request_packet = json.dumps({"request_type":"serve_model","model":modelid,"config_file":configid})
#     request_packet_s = str(request_packet)
#     obj = RabbitMQ()
#     obj.send("","AD_SM",request_packet)
