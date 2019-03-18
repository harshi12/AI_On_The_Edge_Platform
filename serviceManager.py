from queue_req_resp import RabbitMQ
from thread import th
import json
RMQ = RabbitMQ()


class serviceManager:
    def __init__(self):
        th(self.receive_AD_input,'', "AD_SM")
        th(self.receive_scheduler_input, '', "Scheduler_SM")

    def process_AD_input(self, ch, method, properties, body):
        ip_list = ['127.0.0.1']
        to_send = {"No_Hosts" : 1, "IPs" : ip_list, "Model_Link" : str(body)}
        to_send = json.loads(to_send)
        RMQ.send()

    def sendtoScheduler(self, ch, method, properties, body):
        RMQ.send('', "SM_Scheduler")

    def receive_AD_input(self, exchange, key):
        RMQ.receive(self.sendtoScheduler, exchange, key)

    def receive_scheduler_input(self, exchange, key):
        RMQ.receive(self.process_scheduler_input, exchange, key)

    def process_scheduler_input(self, ch, method, properties, body):

