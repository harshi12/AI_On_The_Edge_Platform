import sys

from pathlib import Path
home = str(Path.home())
path = home+'/Platform/'
sys.path.insert (0, path)

from apscheduler.schedulers.background import BackgroundScheduler
import threading
import xml.etree.ElementTree as ET
import requests
import zipfile
import json
import os
import time
import datetime
import json

from queue_req_resp import *
from Registry.Registry_API import *


class PlatformScheduler:
    def __init__(self):
        self.MODULES_REQ_QUEUE = "modules_scheduler"
        self.RBMQ = RabbitMQ()
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()


    def schedule_service(self, service_id):
        req = {}
        req["opcode"] = "SCHEDULE_SERVICE"
        req["service_id"] = service_id
        json_req = json.dumps(req)
        self.RBMQ.send("", self.MODULES_REQ_QUEUE, json_req)

    def trigger_service(self, _id, category):
        req = {}
        req["Request_Type"] = category[:-1] + "_Submit"
        if category == "Models":
            req["Model_ID"] = _id
        else:
            req["Service_ID"] = _id
        req["Instances"] = 1
        json_req_str = json.dumps(req)
        print (f"[Scheduler] sending request to HM {req}")
        self.RBMQ.send("", "SCHED_HM", json_req_str)


    def handle_modules_requests(self, ch, method, properties, body):
        if not isinstance(body, str):
            body = body.decode()

        body = json.loads(body)
        print (f"[Scheduler] got request: {body}")
        if body["opcode"] == "SCHEDULE_SERVICE":
            service_id = body["service_id"]
            registry = Registry_API()
            registry.Read_Service_Link_Info([service_id], "SCHED_RG", "RG_SCHED")

            link = self.RBMQ.receive_nonblock("", "RG_SCHED")
            if not isinstance(link, str):
                link = link.decode()

            link = json.loads(link)

            print (f"[Scheduler] got link from register: {link}")

            link = link[service_id]

            print (f"[Scheduler] got link from register: {link}")

            #link = "~/Platform/1/2/Services/Counter_Service"
            link = home + link[1:]
            rootLink = link #get the mount path of the service

            fw_slash_idx = link.rfind('/')
            name = rootLink[fw_slash_idx + 1: ]
            rootLink = rootLink[: fw_slash_idx]

            fw_slash_idx = rootLink.rfind('/')
            category = rootLink[fw_slash_idx + 1: ]
            rootLink = rootLink[: fw_slash_idx]

            if category == "Models":
                prodConfig = rootLink + '/Config/' + name + '_Model_DeployConfig.xml'
            else:
                prodConfig = rootLink + '/Config/' + name + '_DeployConfig.xml'

            print (f"[Scheduler] prodConfig: {prodConfig}")
            xml_element_tree = ET.parse(prodConfig)       
            root = xml_element_tree.getroot()
            for node in root.iter('Scheduling'):
                for elements in node:
                    if elements.tag == 'TriggerInterval':
                        trigger_interval = elements.text
                    elif elements.tag == 'StartTime':
                        start_time = elements.text
                    elif elements.tag == 'EndTime':
                        end_time = elements.text
                    elif elements.tag == 'UpTime':
                        up_time = elements.text
                    else:
                        print ("It can't reach here")

            if trigger_interval != "None":
                trigger_interval = int(trigger_interval)
                self.scheduler.add_job(self.trigger_service, 'interval', seconds=trigger_interval, args=[service_id, category])
            elif start_time != "None":
                # TODO: Add job to trigger service at start_time
                #start_time = int(start_time)
                #self.scheduler.add_job()
                pass
            elif end_time != "None":
                # TODO: Add job to end service at end_time
                pass
            elif up_time != "None":
                # this is redundant
                pass
            else:
                print (f"[Scheduler] Doing nothing for service: {name}")

    def recv_modules_requests(self):
        self.RBMQ.receive(self.handle_modules_requests, '', self.MODULES_REQ_QUEUE)


if __name__ == "__main__":
    platform_scheduler = PlatformScheduler()
    threading.Thread(target = platform_scheduler.recv_modules_requests).start()
