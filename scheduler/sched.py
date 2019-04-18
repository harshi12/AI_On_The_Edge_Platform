import sys

from pathlib import Path
home = str(Path.home())
path = home+'/Platform/'
sys.path.insert (0, path)

import threading

from queue_req_resp import *

class PlatformScheduler:
    def __init__(self):
        self.MODULES_REQ_QUEUE = "modules_scheduler"
        self.RBMQ = RabbitMQ()

    def schedule_services(self, service_ids):
        req = {}
        req["opcode"] = "SCHEDULE_SERVICES"
        req["service_ids"] = service_ids
        json_req = json.dumps(req)
        self.RBMQ.send("", self.MODULES_REQ_QUEUE, json_req)

    def recv_modules_requests_util(self, func):
        self.RBMQ.receive(func, '', self.MODULES_REQ_QUEUE)

    def recv_modules_requests(self, func):
        threading.Thread(target = self.recv_modules_requests_util, args = (func,)).start()
