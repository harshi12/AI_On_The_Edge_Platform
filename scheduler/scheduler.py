from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.schedulers import Scheduler

import requests
import sys
import zipfile
import json
import os
import time
import datetime
from queue_req_resp import RabbitMQ

ALWAYS_RUNNING = 1
DEPLOYMENT_TIME = 20
KILL_TIME = 10

scheduler = BackgroundScheduler()
scheduler.start()

#scheduler2 = Scheduler()
#scheduler2.start()


############## Download Zip file from GDrive #########################
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def download_and_read_file(file_id):
    download_path = "./" + file_id
    try:
        os.makedirs(download_path)
    except:
        pass

    local_file_path = download_path + '/model.zip'

    #print("File id: ", file_id)
    #print("Destination: ", destination_path)
    download_file_from_google_drive(file_id, local_file_path)

    # Unzipping the file
    zip_ref = zipfile.ZipFile(local_file_path, 'r')
    zip_ref.extractall(download_path)
    zip_ref.close()

    config_filename = "config.json"
    config_file_path = download_path + "/model/" + config_filename

    with open(config_file_path) as f:
        data = json.load(f)

    serviceType=int(data["schedule_info"]["service_type"])
    starttime=int(data["schedule_info"]["parameters"]["start_time"])
    endtime=int(data["schedule_info"]["parameters"]["end_time"])
    streamType=int(data["schedule_info"]["stream_type"])
    stream_interval=int(data["schedule_info"]["stream_interval"])

    return serviceType, starttime, endtime, streamType, stream_interval


def deploy_service(serviceName):
    # [RabittMQ] -> ServiceManager: "serviceName deploy"
    sm_data = {}
    sm_data["request_type"] = "deploy"
    sm_data["model"] = serviceName
    json_sm_data = json.dumps(sm_data)
    RBMQ.send("", "Scheduler_SM", json_sm_data)


def kill_service(serviceName):
    # [RabittMQ] -> ServiceManager: "serviceName kill"
    sm_data = {}
    sm_data["request_type"] = "kill"
    sm_data["model"] = serviceName
    json_sm_data = json.dumps(sm_data)
    RBMQ.send("", "Scheduler_SM", json_sm_data)


def inference_live_data(serviceName):
    # [RabittMQ] -> ServiceManager: "serviceName inference live data"
    sm_data = {}
    sm_data["request_type"] = "inference_live"
    sm_data["model"] = serviceName
    json_sm_data = json.dumps(sm_data)
    RBMQ.send("", "Scheduler_SM", json_sm_data)

def inference_batch_data(serviceName):
    # [RabittMQ] -> ServiceManager: "serviceName read data batch"
    sm_data = {}
    sm_data["request_type"] = "inference_batch"
    sm_data["model"] = serviceName
    json_sm_data = json.dumps(sm_data)
    RBMQ.send("", "Scheduler_SM", json_sm_data)

def remove_job(job):
    job.remove()

def service_configuration(ch, method, properties, body):
    print (body.decode())
    body = body.decode()
    sm_data = json.loads(body)
    serviceName = sm_data["model"]

    serviceType, starttime, endtime, streamType, stream_interval = download_and_read_file(serviceName)

    # serviceType
    if serviceType == ALWAYS_RUNNING:
        deploy_service(serviceName)

        if streamType == 1:
            stream_interval %= 100
            time.sleep(DEPLOYMENT_TIME)
            inference_batch_data(serviceName)
            scheduler.add_job(inference_batch_data, 'interval', minutes=stream_interval, args=[serviceName])
        else:
            inference_live_data(serviceName)
    else:
        st_date = datetime.datetime.now()
        st_date = st_date.replace(hour=(int(starttime / 100)), minute=(starttime % 100), second = 0)
        scheduler.add_job(deploy_service, 'date', run_date=st_date + datetime.timedelta(seconds=3), args=[serviceName])

        if endtime != 0:
            end_date = datetime.datetime.now()
            end_date = st_date.replace(hour=(int(endtime / 100)), minute=(endtime % 100), second = 0)
            scheduler.add_job(kill_service, 'date', run_date=end_date, args=[serviceName])

        if streamType == 1:
            stream_interval %= 100
            #scheduler.add_job(inference_batch_data, 'date', run_date=datetime(2019, 03, 18, st_hour, st_min, 5), args=[serviceName])
            #job = scheduler2.add_interval_job(inference_batch_data, minutes = stream_interval, start_date = st_date + datetime.timedelta(seconds=DEPLOYMENT_TIME), args=[serviceName])

            if endtime != 0:
                scheduler.add_job(remove_job, 'date', run_date=end_date + datetime.timedelta(seconds=KILL_TIME), args=[job])

            #scheduler.add_job(inference_batch_data, 'interval', minutes=stream_interval, args=[serviceName])
        else:
            job = scheduler.add_job(inference_live_data, 'date', run_date=st_date + datetime.timedelta (seconds=DEPLOYMENT_TIME), args=[serviceName])


RBMQ = RabbitMQ()
while True:
    RBMQ.receive(service_configuration, "", "SM_Scheduler")
