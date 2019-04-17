import os
import json
from queue_req_resp import RabbitMQ
from Registry_API import Registry_API
import threading
import time
import sys

class Monitor:

    def __init__(self, Local_Password):
        self.Host_Info = {}
        self.Gateway_Info = {}
        self.Module_Info = {}
        self.Service_info = {}
        self.Local_Password = Local_Password

    def Read_Host_Info(self):
        # Send Read request to registry , response will be in MTHC_RG queue
        Registry_obj.Read_Host_Creds([],  "MTHC_RG", "RG_MTHC")

    def Read_Gateway_Info(self):
        # Send Read request to registry , response will be in MTHC_RG queue
        Registry_obj.Read_Gateway_Creds([],  "MTGC_RG", "RG_MTGC")

    def Read_Service_Info(self):
        # Send Read request to registry , response will be in MTSI_RG queue
        Registry_obj.Read_Service_Inst_Info([], "MTSI_RG", "RG_MTSI")

    def Read_Platform_Module_Info(self):
        # Send Read request to registry , response will be in MTPI_RG queue
        Registry_obj.Read_Platform_Module_Info([], "MTPI_RG", "RG_MTPI")

    def Check_Model(self, host):

        IP = host[0]
        Port = host[1]
        Status = host[2]

        print("nmap -p " + Port + " " + IP + " | grep open")
        result = os.system("nmap -p " + Port + " " + IP + " | grep open")
        print("Check Model Result:", result)

        if result != 0:
            return 0
        else:
            return 1

    def Check_Service(self, host):

        IP = host[0]
        Port = host[1]
        Status = host[2]
        Pid = host[3]

        Username = self.Host_Info[IP]["Username"]
        Password = self.Host_Info[IP]["Password"]

        if os.path.exists("ServiceOutput.txt"):
            os.remove("ServiceOutput.txt")
        cmd="sshpass -p " + Password + " ssh -o StrictHostKeyChecking no " + Username + "@" + IP + " \"exit\""
        cmd = "sshpass -p "+ Password + " ssh " + Username + "@" + IP + " ps -fp " + str(Pid) + " | wc -l > ServiceOutput.txt"
        print("Check Service Command: ", cmd)
        os.system(cmd)

        with open("ServiceOutput.txt") as f:
            content = f.read().strip()

        result = int(content)
        print("Check Service Result: ", result)

        if result == 1:
            return 0
        else:
            return 1

    def Check_Platform_Host(self, Module_ID, Host_type):

        Ip = self.Module_Info[Module_ID][Host_type]["IP"]
        Username = self.Module_Info[Module_ID][Host_type]["Username"]
        Password = self.Module_Info[Module_ID][Host_type]["Password"]
        Pid = self.Module_Info[Module_ID][Host_type]["Pid"]

        if os.path.exists("PlatformOutput.txt"):
            os.remove("PlatformOutput.txt")

        cmd="sshpass -p " + Password + " ssh -o StrictHostKeyChecking no " + Username + "@" + IP + " \"exit\""
        cmd = "sshpass -p "+ Password + " ssh " + Username + "@" + Ip + " ps -fp " + str(Pid) + " | wc -l > PlatformOutput.txt"
        print("Command: ", cmd)
        os.system(cmd)

        with open("PlatformOutput.txt") as f:
            content = f.read().strip()

        result = int(content)
        print("Check Platform Module Result: ", result)
        return result

    def Check_Platform_Module(self):
        #For every platform module running, check status
        for module in self.Module_Info.keys():

            pri_result = self.Check_Platform_Host(module, "Primary")
            print("Primary result: ", pri_result)

            if pri_result == 1:
                rec_result = self.Check_Platform_Host(module, "Recovery")
                print("Recovery result: ", rec_result)

                if rec_result == 1:
                    print("Both hosts are down. SORRY!")
                else:
                    msg = {"Module_ID" : module }
                    json_msg = json.dumps(msg)

            		msg_obj.send("", "MT_RM", json_msg)
                    print("Msg sent to Recovery Manager: ", json_msg)
            else:
                print("Primary host is running\n")

        self.Read_Platform_Module_Info()

def callback_gc(ch, method, properties, body):

    body = body.decode("utf-8").replace('\0', '')
    M.Gateway_Info = json.loads(body)
    print("\nReceiving Gateway Credentials: ", M.Gateway_Info)

    t_si = threading.Thread(target=M.Read_Service_Info)
    t_si.start()

    t_pi = threading.Thread(target=M.Read_Platform_Module_Info)
    t_pi.start()

def callback_hc(ch, method, properties, body):
    body = body.decode("utf-8").replace('\0', '')
    M.Host_Info = json.loads(body)
    print("\nReceiving Host Credentials: ", M.Host_Info)

    M.Read_Gateway_Info()

def callback_si(ch, method, properties, body):
    body = body.decode("utf-8").replace('\0', '')
    M.Service_Info = json.loads(body)
    print("\nReceiving Service Info: ", M.Service_Info)

    for service in M.Service_Info.keys():

        Instances_list = M.Service_Info[service]

        request_HM_GW = {}
        request_HM_GW["Gateway_IPs"] = []
        request_HM_HT = {}

        model_instances = 0
        service_instances = 0

        for i in range(len(Instances_list)):
            if Instances_list[i][4] == "model":

                IP = Instances_list[i][0]

                model_result = M.Check_Model(Instances_list[i])
                service_result = 1
                if i+1 < len(Instances_list) and Instances_list[i+1][4] == "exe" and Instances_list[i+1][5] == Instances_list[i][5]:
                    service_result = M.Check_Service(Instances_list[i+1])

                if model_result==0 or service_result==0:
                    if Instances_list[i][2] == "Up" :
                        if IP in M.Gateway_Info.keys():
                            request_HM_GW["Request_Type"] = "Gateway_Deploy"
                            request_HM_GW["Gateway_IPs"].append([IP])
                            request_HM_GW["Service_ID"] = service
                        else:
                            model_instances = model_instances + 1
                        Instances_list[i][2] = "Down"
                i = i + 1

            elif Instances_list[i][4] == "exe":

                service_result = M.Check_Service(Instances_list[i])
                if service_result == 0 :
                    if Instances_list[i][2] == "Up" :
                        service_instances = service_instances + 1
                        Instances_list[i][2] = "Down"

        if model_instances >  0:
            request_HM_HT["Request_Type"] = "Model_Submit"
            request_HM_HT["Model_ID"] = service
            request_HM_HT["Instances"] = str(model_instances)

            request_HM_HT_json = json.dumps(request_HM_HT)
            msg_obj = RabbitMQ()
            msg_obj.send("", "MT_HM", request_HM_HT_json)
            print("Model start on host Request sent to HM: ", request_HM_HT_json)

        if service_instances >  0:
            request_HM_HT["Request_Type"] = "Service_Submit"
            request_HM_HT["Model_ID"] = service
            request_HM_HT["Instances"] = str(service_instances)

            request_HM_HT_json = json.dumps(request_HM_HT)
            msg_obj = RabbitMQ()
            msg_obj.send("", "MT_HM", request_HM_HT_json)
            print("Service start Request sent to HM: ", request_HM_HT_json)

        if len(request_HM_GW["Gateway_IPs"]) > 0:
            request_HM_GW_json = json.dumps(request_HM_GW)
            msg_obj = RabbitMQ()
            msg_obj.send("", "MT_HM", request_HM_GW_json)
            print("Model start on Gateway Request sent to HM: ", request_HM_GW_json)

    M.Read_Service_Info()

def callback_pi(ch, method, properties, body):
    body = body.decode("utf-8").replace('\0', '')
    M.Module_Info = json.loads(body)
    print("\nReceiving Platform  Module Info: ", M.Module_Info)
    M.Check_Platform_Module()

def Recieve_from_RG_MTHC():
    msg_obj.receive(callback_hc, "", "RG_MTHC")

def Recieve_from_RG_MTGC():
    msg_obj.receive(callback_gc, "", "RG_MTGC")

def Recieve_from_RG_MTSI():
    msg_obj.receive(callback_si, "", "RG_MTSI")

def Recieve_from_RG_MTPI():
    msg_obj.receive(callback_pi, "", "RG_MTPI")


Registry_obj = Registry_API()
msg_obj = RabbitMQ()

local_password = sys.argv[1]
M = Monitor(local_password)

t2 = threading.Thread(target=Recieve_from_RG_MTHC)
t2.start()

t3 = threading.Thread(target=Recieve_from_RG_MTGC)
t3.start()

t4 = threading.Thread(target=Recieve_from_RG_MTSI)
t4.start()

t5 = threading.Thread(target=Recieve_from_RG_MTPI)
t5.start()

M.Read_Host_Info()
