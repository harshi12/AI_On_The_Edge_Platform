from queue_req_resp import RabbitMQ
from threading import Thread
import requests
import ast
# from _thread    
import json
RMQ = RabbitMQ()

model_port_map = {}
model_IPS = []
model_port_index = {}


class serviceManager:
    def __init__(self):
        t1 = Thread(target = self.receive_AD_input, args = ('', "AD_SM"))
        t2 = Thread(target = self.receive_scheduler_input, args = ('', "Scheduler_SM"))
        t3 = Thread(target = self.receive_DM_input, args = ('', "Docker_SM"))
        t1.start()
        t2.start()
        t3.start()

    def process_Model_Input(self, ch, method, properties, body):
        # print("*****************",body)
        data = json.loads(body)
        # print(data)
        # print("Data received successfully")
        # print("################################")
        # print("parsed")
        return data


    def receive_InputStream_input(self, exchange, key):
        body = RMQ.receive_nonblock(exchange, key)
        body = body.decode()
        data = json.loads(body)
        data = ast.literal_eval(data)
        print("Data Before:",data)
        print("Data Type: ",type(data))
        return data

    def receive_DM_input(self,exchange, key):
        RMQ.receive(self.process_DM_Input, exchange, key)

    def process_DM_Input(self, ch, method, properties, body):
        global model_port_map
        data = json.loads(body)
        ack_response = data["ack_response"]
        for key in ack_response.keys():
            model_port_map[key] = ack_response[key]

    def sendtoScheduler(self, ch, method, properties, body):
        print("data from AD %r"%body)
        RMQ.send('', "SM_Scheduler",body)

    def receive_AD_input(self, exchange, key):
        print("In thread AD_input")
        RMQ.receive(self.sendtoScheduler, exchange, key)

    def receive_scheduler_input(self, exchange, key):
        print("receive_scheduler_input")
        while True:
            print("here")
            RMQ.receive(self.process_scheduler_input, exchange, key)

    def process_scheduler_input(self, ch, method, properties, body):
        print("1")
        data = json.loads(body)
        print(body)
        if data["request_type"] == 'deploy':
            message = {"Request_type" : "Deploy", "Link" : data["model"], "No_Hosts" : 1, "IPs" : ["192.168.43.137"]}
            global model_IPS
            model_port_index[data["model"]] = 0
            model_IPS = message["IPs"]
            message = json.dumps(message)   
            RMQ.send("","SM_Docker", message)

        elif data["request_type"] == 'kill':
            pass

        elif data["request_type"]    == "inference_batch":
            print("Inference Batch Request")
            final_batch_test_data = {}
            batch_test_data = self.receive_InputStream_input("", "Model1_Input")

            final_batch_test_data['signature_name'] = 'model'
            final_batch_test_data['instances'] = batch_test_data['data']

            print("Testing Data:")
            print(final_batch_test_data)

            model_name = data["model"]
            model_ports = model_port_map[model_name]
            
            i = model_port_index[model_name]
            i = i%len(model_ports)

            print("Prediction model sent to", model_IPS[i],":",model_ports[i])

            headers = {"content-type": "application/json"}
            json_response = requests.post('http://'+model_IPS[i]+':'+model_ports[i]+'/v1/models/'+model_name+':predict', data=final_batch_test_data, headers=headers)
            i += 1
            print (json_response.text)

            RMQ.send("", "Model1_Output", json_response.text)

        elif data["request_type"] == "inference_live":
            pass

        return

# def myfun(self, ch, method, properties, body):
#     print("Received Data: %r"%body)

if __name__ == '__main__':
    obj = serviceManager()
    # obj
#     message_ravi = {"Request_type" : "Deploy", "Link" : "This is my Link", "No_Hosts" : 1, "IPs" : ["192.168.43.137"]}
#     message = {"request_type": "serve_model", "model": "1d_jdNRI7Ak-_CSPo6wYUUt0fj0_yKqjb"}
#     message = json.dumps(str(message))
#     RMQ.send("","SM_Scheduler", message)

#     RMQ.receive(myfun, "", "Scheduler_SM")

