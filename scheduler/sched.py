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

    def schedule_service(self, service_id):
        req = {}
        req["opcode"] = "SCHEDULE_SERVICE"
        req["service_id"] = service_id
        json_req = json.dumps(req)
        self.RBMQ.send("", self.MODULES_REQ_QUEUE, json_req)

    def recv_modules_requests_util(self, func):
        self.RBMQ.receive(func, '', self.MODULES_REQ_QUEUE)

    def recv_modules_requests(self, func):
        threading.Thread(target = self.recv_modules_requests_util, args = (func,)).start()
