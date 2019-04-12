from googleapiclient.discovery import build
from oauth2client import client, tools, file
from googleapiclient.http import MediaFileUpload
from queue_req_resp import RabbitMQ
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

def uploadconfig(configpath,configname):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    drive_service = build('drive', 'v3', http=creds.authorize(Http()))

    folder_id = '1c63s9RQ_xrb58BGXhyvWQnJEasfc0Vgn'
    file_metadata = { 'name':modelname,'parents': [folder_id]}
    media = MediaFileUpload(filepath, mimetype='application/vnd.google-apps.script+json', resumable=True)
    DATA = drive_service.files().create(body=file_metadata,media_body=media,fields='id').execute()
    did = DATA.get('id')
    return did

def send_to_service_manager(modelid,configid):
    request_packet = json.dumps({"request_type":"serve_model","model":modelid,"config_file":configid})
    request_packet_s = str(request_packet)
    obj = RabbitMQ("192.168.43.173")
    obj.send("","AD_SM",request_packet_s)
