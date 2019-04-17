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
        self.Module_Info = {}
        self.Model_Info = {}
        self.Service_info = {}
        self.Local_Password = Local_Password

    def Read_Host_Info(self):
        # Send Read request to registry , response will be in MTHC_RG queue
        Registry_obj.Read_Host_Creds([],  "MTHC_RG", "RG_MTHC")

    def Read_Model_Info(self):
        # Send Read request to registry , response will be in MTMI_RG queue
        Registry_obj.Read_Model_Inst_Info([], "MTMI_RG", "RG_MTMI")

    def Read_Service_Info(self):
        # Send Read request to registry , response will be in MTSI_RG queue
        Registry_obj.Read_Service_Inst_Info([], "MTSI_RG", "RG_MTSI")

    def Read_Platform_Module_Info(self):
        # Send Read request to registry , response will be in MTPI_RG queue
        Registry_obj.Read_Platform_Module_Info([], "MTPI_RG", "RG_MTPI")

    def Check_Model(self):

        #For every model running on platform, check status
        for model in self.Model_Info.keys():
            Down_Instances = 0
            Write_Reg = 0
    		#For every ip, check if the model is running
            for host in self.Model_Info[model]:
                IP = host[0]
                Port = host[1]
                Status = host[2]

                print("nmap -p " + Port + " " + IP + " | grep open")
                result = os.system("nmap -p " + Port + " " + IP + " | grep open")
                print("Check Model Result:", result)

    			#If not running
                if result != 0:
                    if Status == "Up":
                        Down_Instances += 1
    					#Write in Registry
                        host[2] = "Down"
                        Write_Reg = 1
                        print("Writing in Registry NOT RUNNING, STATUS UP")
                    print(" NOT RUNNING, STATUS DOWN")
                else:
                    if Status == "Down":
    					#Write Registry
                        host[2] = "Up"
                        Write_Reg = 1
                        print("Writing in Registry RUNNING, STATUS DOWN")
                    print("RUNNING, STATUS UP")

            if Write_Reg == 1:
                Registry_obj.Write_Model_Inst_Info(model, self.Model_Info[model], "MTMI_RG")

            if Down_Instances > 0:
    			#Send request to Host Manager
                request_MT = {"Request_Type": "Model_Submit","Model_ID" : model,"Instances" : str(Down_Instances)}
                request_MT_json = json.dumps(request_MT)
                msg_obj = RabbitMQ()
                msg_obj.send("", "MT_HM", request_MT_json)
                print("Request sent to HM: ", request_MT_json)

        self.Read_Model_Info()

    def Check_Service(self):

        #For every service running on platform, check status
        for service in self.Service_Info.keys():
            Down_Instances = 0
            Write_Reg = 0
    		#For every ip, check if the service is running
            for host in self.Service_Info[service]:
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

    			#If not running
                if result == 1:
                    if Status == "Up":
                        Down_Instances += 1
    					#Write in Registry
                        host[2] = "Down"
                        Write_Reg = 1
                        print("Writing in Registry NOT RUNNING, STATUS UP")
                    print(" NOT RUNNING, STATUS DOWN")
                else:
                    if Status == "Down":
    					#Write Registry
                        host[2] = "Up"
                        Write_Reg = 1
                        print("Writing in Registry RUNNING, STATUS DOWN")
                    print("RUNNING, STATUS UP")

            if Write_Reg == 1:
                Registry_obj.Write_Service_Inst_Info(service, self.Service_Info[service], "MTSI_RG")

            if Down_Instances > 0:
    			#Send request to Host Manager
                request_MT = {"Request_Type": "Service_Submit","Service_ID" : service,"Instances" : str(Down_Instances)}
                request_MT_json = json.dumps(request_MT)
                msg_obj = RabbitMQ()
                msg_obj.send("", "MT_HM", request_MT_json)
                print("Request sent to HM: ", request_MT_json)

        self.Read_Service_Info()

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


def callback_hc(ch, method, properties, body):
    body = body.decode("utf-8").replace('\0', '')
    M.Host_Info = json.loads(body)
    print("\nReceiving Host Credentials: ", M.Host_Info)

    t_mi = threading.Thread(target=M.Read_Model_Info)
    t_mi.start()

    t_si = threading.Thread(target=M.Read_Service_Info)
    t_si.start()

    t_pi = threading.Thread(target=M.Read_Platform_Module_Info)
    t_pi.start()

def callback_mi(ch, method, properties, body):
    body = body.decode("utf-8").replace('\0', '')
    M.Model_Info = json.loads(body)
    print("\nReceiving Model Info: ", M.Model_Info)
    M.Check_Model()

def callback_si(ch, method, properties, body):
    body = body.decode("utf-8").replace('\0', '')
    M.Service_Info = json.loads(body)
    print("\nReceiving Service Info: ", M.Service_Info)
    M.Check_Service()

def callback_pi(ch, method, properties, body):
    body = body.decode("utf-8").replace('\0', '')
    M.Module_Info = json.loads(body)
    print("\nReceiving Platform  Module Info: ", M.Module_Info)
    M.Check_Platform_Module()

def Recieve_from_RG_MTHC():
    msg_obj.receive(callback_hc, "", "RG_MTHC")

def Recieve_from_RG_MTMI():
    msg_obj.receive(callback_mi, "", "RG_MTMI")

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

t3 = threading.Thread(target=Recieve_from_RG_MTMI)
t3.start()

t4 = threading.Thread(target=Recieve_from_RG_MTSI)
t4.start()

t5 = threading.Thread(target=Recieve_from_RG_MTPI)
t5.start()

M.Read_Host_Info()

# t1 = threading.Thread(target=main)
# t1.start()
