from apscheduler.schedulers.background import BackgroundScheduler

import requests
import sys
import zipfile
import json
import os
from queue_req_resp import RabbitMQ

ALWAYS_RUNNING = 1

scheduler = BackgroundScheduler()
scheduler.start()


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
            inference_batch_data(serviceName)
            scheduler.add_job(inference_batch_data, 'interval', minutes=stream_interval, args=[serviceName])
        else:
            inference_live_data(serviceName)
    else:
        st_hour = startTime / 100
        st_min = startTime % 100
        scheduler.add_job(deploy_service, 'date', run_date=datetime(2019, 3, 18, st_hour, st_min, 0), args=[serviceName])
        scheduler.add_job(kill_service, 'date', run_date=datetime(2019, 3, 18, st_hour, st_min, 0), args=[serviceName])

        #if streamType == 1:
        #    stream_interval %= 100
        #    scheduler.add_job(inference_batch_data, 'date', run_date=datetime(2019, 03, 18, st_hour, st_min, 5), args=[serviceName])
        #    scheduler.add_job(inference_batch_data, 'interval', minutes=stream_interval, args=[serviceName])
        #else:
        job = scheduler.add_job(inference_live_data, 'date', run_date=datetime(2019, 3, 18, st_hour, st_min, 5), args=[serviceName])


RBMQ = RabbitMQ()
while True:
    RBMQ.receive(service_configuration, "", "SM_Scheduler")
