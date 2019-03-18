from queue_req_resp import RabbitMQ
from thread import th
import json
RMQ = RabbitMQ()

model_port_map = {}

class serviceManager:
    def __init__(self):
        th(self.receive_AD_input,'', "AD_SM")
        th(self.receive_scheduler_input, '', "Scheduler_SM")
        th(self.receive_DM_input, '', "Docker_SM")

    def receive_DM_input(self,"", key):
        RMQ.receive(self.process_DM_Input, exchange, key)

    def process_DM_Input(self, ch, method, properties, body):
        global model_port_map
        data = json.loads(body)
        ack_response = data["Ack_Deploy"]
        for key in ack_response.keys():
            model_port_map[key] = ack_response[key]

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
        data = json.loads(body)
        if data["request_type"] == 'deploy':
            message = {"Request_type" : "Deploy", "Link" : data[service_name], "No_Hosts" : 1, "IPs" : ["192.168.43.137"]}
            message = json.dumps(message)
            RMQ.send("","SM_Docker", message)

        else if data["request_type"] == 'kill':
            pass

        else if data["request_type"] == "inference_batch":
            pass

        else if data["request_type"] == "inference_live":
            pass
