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
port_list = []
live_threads = {}
thread_stop_flag = {}

class serviceManager:
    def __init__(self):
        self.lock = threading.Lock()
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
        # print("################################")
        # print("parsed")
        return data


    def receive_InputStream_input(self, exchange, key):
        body = RMQ.receive_nonblock(exchange, key)
        body = body.decode()
        data = json.loads(body)
        data = ast.literal_eval(data)
        print("Data received successfully")
        # print("Data Before:",data)
        # print("Data Type: ",type(data))
        return data

    def receive_DM_input(self,exchange, key):
        print("In docker receiver queue")
        RMQ.receive(self.process_DM_Input, exchange, key)

    def process_DM_Input(self, ch, method, properties, body):
        global model_port_map
        data = json.loads(body)
        data = ast.literal_eval(data)
        print("Docker data",data)
        global port_list
        ack_response = data["Ack"]
        print("Docker Manager Response: ", ack_response)
        model_name = ack_response["Model"]
        model_port_map[model_name] = ack_response["IP:Port"]

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

    def get_thread_id(self): 
        # returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id

    def inference_LiveData(self, model_name):
        thread_id = self.get_thread_id()
        while True:
            if thread_stop_flag[thread_id]:
                break

            body = RMQ.receive_nonblock("", "Model1_Input")
            if body is None:
                continue

            body = body.decode()
            data = json.loads(body)
            data = ast.literal_eval(data)
            print("Data received successfully")
            print(data)
            data_rows = data["data"]

            for i in range(len(data_rows)):
                test_data = {}
                test_data["signature_name"] = "model"
                test_data["instances"] = [data_rows[i]]
                test_data = json.dumps(test_data)

                service_ip_port = ""

                print("Acquiring Lock in thread")
                self.lock.acquire()
                try:
                    i = model_port_index[model_name]
                    service_ip_port = model_ip_ports[i]
                    i = (i+1) % len(model_ip_ports)
                    model_port_index[model_name] = i
                finally:
                    self.lock.release()
                    print("Lock released in thread")

                print("Prediction model sent to", service_ip_port)

                headers = {"content-type": "application/json"}
                request_string = str('http://'+service_ip_port+'/v1/models/'+model_name+':predict')
                print("Request String", request_string)
                json_response = requests.post(request_string, data=final_batch_test_data, headers=headers)
                print("After making REST call")
                # i = (i+1) % len(model_ip_ports)
                # self.lock.acquire()
                # try:
                #     model_port_index[model_name] = i
                #     print("IP:Port index updated in thread!")
                # finally:
                #     self.lock.release()

                print (json_response.text)

                RMQ.send("", "Model1_Output", json_response.text)

    def process_scheduler_input(self, ch, method, properties, body):
        print("1")
        data = json.loads(body)
        print(body)
        model_name = data["model"]

        if data["request_type"] == 'deploy':
            message = {"Request_type" : "Deploy", "Link" : data["model"], "No_Hosts" : 1, "IPs" : ["192.168.43.103"]}
            global model_IPS
            model_port_index[model_name] = 0
            model_IPS = message["IPs"]
            message = json.dumps(message)   
            RMQ.send("","SM_Docker", message)

        elif data["request_type"] == 'kill':
            message = {"Request_type" : "Kill", "Link" : data["model"], "No_Hosts" : 1, "IPs" : ["192.168.43.103"]}
            thread_id = live_threads[model_name]
            thread_stop_flag[thread_id] = 1
            
        elif data["request_type"]    == "inference_batch":
            print("Inference Batch Request")
            final_batch_test_data = {}
            batch_test_data = self.receive_InputStream_input("", "Model1_Input")

            final_batch_test_data["signature_name"] = "model"
            final_batch_test_data["instances"] = batch_test_data['data']

            print("Testing Data:")
            print(final_batch_test_data)

            final_batch_test_data = json.dumps(final_batch_test_data)

            # model_name = data["model"]
            model_ip_ports = model_port_map[model_name]
            
            service_ip_port = ""
                
            print("Acquiring Lock in main")
            self.lock.acquire()
            try:
                i = model_port_index[model_name]
                service_ip_port = model_ip_ports[i]
                i = (i+1) % len(model_ip_ports)
                model_port_index[model_name] = i
            finally:
                self.lock.release()
                print("Lock released in main")

            print("Prediction model sent to", service_ip_port)

            # print("Prediction model sent to", model_ip_ports[i])

            headers = {"content-type": "application/json"}
            request_string = str('http://'+service_ip_port+'/v1/models/'+model_name+':predict')
            print("Request String", request_string)
            json_response = requests.post(request_string, data=final_batch_test_data, headers=headers)
            print("After making REST call")
            # print("Acquiring Lock in main")
            # i += 1
            # self.lock.acquire()
            # try:
            #     model_port_index[model_name] = i
            #     print("IP:Port index updated in main!")
            # finally:
            #     self.lock.release()
            #     print("Lock released in main")
            # model_port_index[model_name] = i
            print (json_response.text)

            RMQ.send("", "Model1_Output", json_response.text)

        elif data["request_type"] == "inference_live":
            global thread_stop_flag
            global live_threads

            print("In inference live")
            final_batch_test_data = {}
            # model_name = data["model"]

            t5 = Thread(target = self.inference_LiveData, args = (model_name))
            t5.start()
            thread_stop_flag[t5] = 0 #0 - thread is running, 1 - kill the thread
            live_threads[model_name] = t5
            
        return


if __name__ == '__main__':
    obj = serviceManager()

