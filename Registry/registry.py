from queue_req_resp import RabbitMQ
import json
import threading
import sys
import time

RMQ = 0

class Registry:

    def __init__(self):
        self.Storage_info = {}
        self.Service_link_info = {}
        self.Service_inst_info = {}
        self.App_inst_info = {}
        self.Host_Creds = {}
        self.Gateway_Creds = {}
        self.Platform_Module_Info = {}

    def Restore_DS(self):

        with open('Storage_info.json') as json_file:
            self.Storage_info = json.load(json_file)
        with open('Service_link_info.json') as json_file:
            self.Service_link_info = json.load(json_file)
        with open('Service_inst_info.json') as json_file:
            self.Service_inst_info = json.load(json_file)
        with open('App_inst_info.json') as json_file:
            self.App_inst_info = json.load(json_file)
        with open('Host_Creds.json') as json_file:
            self.Host_Creds = json.load(json_file)
        with open('Platform_Module_Info.json') as json_file:
            self.Platform_Module_Info = json.load(json_file)
        with open('Gateway_Creds.json') as json_file:
            self.Gateway_Creds = json.load(json_file)

    def Store_DS(self):

        with open('Storage_info.json', 'w') as json_file:
            json.dump(self.Storage_info, json_file)
        with open('Service_link_info.json', 'w') as json_file:
            json.dump(self.Service_link_info, json_file)
        with open('Service_inst_info.json', 'w') as json_file:
            json.dump(self.Service_inst_info, json_file)
        with open('App_inst_info.json', 'w') as json_file:
            json.dump(self.App_inst_info, json_file)
        with open('Host_Creds.json', 'w') as json_file:
            json.dump(self.Host_Creds, json_file)
        with open('Platform_Module_Info.json', 'w') as json_file:
            json.dump(self.Platform_Module_Info, json_file)
        with open('Gateway_Creds.json', 'w') as json_file:
            json.dump(self.Gateway_Creds, json_file)

    def Read_DS(self, DS_Name, DS_Obj):
        Result = {}

        if(DS_Name=="Storage_info"):
            Filter = DS_Obj["App_id"]
            #Filter is a list of App_ids
            if len(Filter)>0:
                for i in range(len(Filter)):
                    App_id = Filter[i]
                    for key in self.Storage_info.keys():
                        if key==App_id:
                            Result[key] = self.Storage_info[key]
            else:
                Result = self.Storage_info
            return Result

        elif(DS_Name=="Service_link_info"):
            Filter = DS_Obj["Service_id"]
            #Filter is a list of App_ids
            if len(Filter)>0:
                for i in range(len(Filter)):
                    Service_id = Filter[i]
                    for key in self.Service_link_info.keys():
                        if key==Service_id:
                           Result[key] = self.Service_link_info[key]
            else:
                Result = self.Service_link_info
            return Result

        elif(DS_Name=="Service_inst_info"):
            Filter = DS_Obj["Service_id"]
            #Filter is a list of App_ids
            if len(Filter)>0:
                for i in range(len(Filter)):
                    Service_id = Filter[i]
                    for key in self.Service_inst_info.keys():
                        if key==Service_id:
                            Result[key] = self.Service_inst_info[key]
            else:
                Result = self.Service_inst_info
            return Result

        elif(DS_Name=="App_inst_info"):
            Filter = DS_Obj["App_id"]
            #Filter is a list of App_ids
            if len(Filter)>0:
                for i in range(len(Filter)):
                    App_id = Filter[i]
                    for key in self.App_inst_info.keys():
                        if key==App_id:
                            Result[key] = self.App_inst_info[key]
            else:
                Result = self.App_inst_info
            return Result

        elif(DS_Name=="Host_Creds"):
            Filter = DS_Obj["Host_IP"]
            #Filter is a list of App_ids
            if len(Filter)>0:
                for i in range(len(Filter)):
                    Host_IP = Filter[i]
                    for key in self.Host_Creds.keys():
                        if key==Host_IP:
                            Result[key] = self.Host_Creds[key]
            else:
                Result = self.Host_Creds
            return Result

        elif(DS_Name=="Gateway_Creds"):
            Filter = DS_Obj["Gateway_IP"]
            #Filter is a list of App_ids
            if len(Filter)>0:
                for i in range(len(Filter)):
                    Host_IP = Filter[i]
                    for key in self.Gateway_Creds.keys():
                        if key==Host_IP:
                            Result[key] = self.Gateway_Creds[key]
            else:
                Result = self.Gateway_Creds
            return Result

        elif(DS_Name=="Platform_Module_Info"):
            Filter = DS_Obj["Module_id"]
            #Filter is a list of App_ids
            if len(Filter)>0:
                for i in range(len(Filter)):
                    Module_id = Filter[i]
                    for key in self.Platform_Module_Info.keys():
                        if key==Module_id:
                            Result[key] = self.Platform_Module_Info[key]
            else:
                Result = self.Platform_Module_Info
            return Result
        else:
            print("Invalid data structure mentioned in read request\n")
            return Result

    def Write_DS(self, DS_Name, DS_Obj):

        if(DS_Name=="Storage_info"):
            for i in range(len(DS_Obj)):
                #Record is a Dict
                Record = DS_Obj[i]
                App_Id = Record["App_id"]

                self.Storage_info[App_Id] = {}

                Model_Link = Record["Model_Link"]
                App_Link = Record["App_Link"]
                Service_Link = Record["Service_Link"]
                Config_Link = Record["Config_Link"]

                self.Storage_info[App_Id]["Model_Link"] = Model_Link
                self.Storage_info[App_Id]["App_Link"] = App_Link
                self.Storage_info[App_Id]["Service_Link"] = Service_Link
                self.Storage_info[App_Id]["Config_Link"] = Config_Link

        elif(DS_Name=="Service_link_info"):
            for i in range(len(DS_Obj)):
                #Record if Dict
                Record = DS_Obj[i]
                Service_id = Record["Service_id"]
                Service_Link = Record["Link"]

                self.Service_link_info[Service_id] = Service_Link

        elif(DS_Name=="Service_inst_info"):
            for i in range(len(DS_Obj)):
                #Record if Dict
                Record = DS_Obj[i]
                Service_Id = Record["Service_id"]

                self.Service_inst_info[Service_Id] = []

                for j in range(len(DS_Obj[i]["Hosts"])):
                    Hosts_List = DS_Obj[i]["Hosts"]
                    Host_IP = Hosts_List[j][0]
                    Host_Port = Hosts_List[j][1]
                    Service_Status = Hosts_List[j][2]
                    Service_Pid = Hosts_List[j][3]
                    Service_Type = Hosts_List[j][4]
                    Instance_No = Hosts_List[j][5]

                    Service_Inst = [Host_IP, Host_Port, Service_Status, Service_Pid, Service_Type, Instance_No]
                    self.Service_inst_info[Service_Id].append(Service_Inst)

        elif(DS_Name=="App_inst_info"):
            for i in range(len(DS_Obj)):
                 #Record if Dict
                 Record = DS_Obj[i]
                 App_Id = Record["App_id"]

                 self.App_inst_info[App_Id] = []

                 for j in range(len(DS_Obj[i]["Hosts"])):
                     Hosts_List = DS_Obj[i]["Hosts"]
                     Host_IP = Hosts_List[j][0]
                     Host_Port = Hosts_List[j][1]
                     App_Status = Hosts_List[j][2]
                     App_Pid = Hosts_List[j][3]

                     App_Inst = [Host_IP, Host_Port, App_Status, App_Pid]
                     self.App_inst_info[App_Id].append(App_Inst)

        elif(DS_Name=="Host_Creds"):
            for i in range(len(DS_Obj)):
                #Record if Dict
                Host_IP = DS_Obj[i]["Host_IP"]
                self.Host_Creds[Host_IP] = {}

                Username = DS_Obj[i]["Username"]
                Password = DS_Obj[i]["Password"]
                self.Host_Creds[Host_IP]["Username"] = Username
                self.Host_Creds[Host_IP]["Password"] = Password

        elif(DS_Name=="Gateway_Creds"):
            for i in range(len(DS_Obj)):
                #Record if Dict
                Host_IP = DS_Obj[i]["Gateway_IP"]
                self.Host_Creds[Host_IP] = {}

                Username = DS_Obj[i]["Username"]
                Password = DS_Obj[i]["Password"]
                self.Host_Creds[Host_IP]["Username"] = Username
                self.Host_Creds[Host_IP]["Password"] = Password

        elif(DS_Name=="Platform_Module_Info"):
            for i in range(len(DS_Obj)):
                #Record if Dict
                Module_id = DS_Obj[i]["Module_id"]
                self.Platform_Module_Info[Module_id] = {}

                Primary = DS_Obj[i]["Primary"]
                Recovery = DS_Obj[i]["Recovery"]

                self.Platform_Module_Info[Module_id]["Primary"] = Primary
                self.Platform_Module_Info[Module_id]["Recovery"] = Recovery

        else :
            print("\nInvalid Data Structure Name\n")

    def Print_DS(self):
        print("\nStorage_info: ", self.Storage_info)
        print("\nService_link_info: ", self.Service_link_info)
        print("\nService_inst_info: ", self.Service_inst_info)
        print("\nApp_inst_info: ", self.App_inst_info)
        print("\nPlatform_Module_Info: ", self.Platform_Module_Info)
        print("\nHost_Creds: ", self.Host_Creds)

# Read JSON from common queue , parse it and call Update_DS/Read_DS function
def callback(ch, method, properties, body):

    global port
    #print ("Receiving from Common queue")
    #body = body.decode("utf-8")
    body = body.decode("utf-8").replace('\0', '')

    #Receiving_Message = json.loads(body).replace('\'','\"')
    Receiving_Message = json.loads(body)
    print("\nReceiving_Message: ", Receiving_Message)

    Request_type = Receiving_Message["Request_Type"]
    DS_Name = Receiving_Message["DS_Name"]

    if(Request_type=="Read"):
        DS_Obj = Receiving_Message["Filter"]
        Sending_Queue = Receiving_Message["Queue_Name"]
        DS_Value = Registry_obj.Read_DS(DS_Name, DS_Obj)
        #print("Read content: ", DS_Value)
        #create JSON and send on temp queue
        DS_Value_json = json.dumps(DS_Value)
        RMQ.send("", Sending_Queue, DS_Value_json)

    if(Request_type=="Write"):
        DS_Obj = Receiving_Message["Value"]
        Registry_obj.Write_DS(DS_Name, DS_Obj)

        #print("\nUpdated Data Structures\n ")
        #Registry_obj.Print_DS()


#TEMP queues Ideally, Common queue will be used which will listen from all modules
def Recieve_from_DM():
    RMQ.receive(callback, "", "DM_RG")

def Recieve_from_SM():
    RMQ.receive(callback, "", "SM_RG")

def Recieve_from_MTHC():
    RMQ.receive(callback, "", "MTHC_RG")

def Recieve_from_MTGC():
    RMQ.receive(callback, "", "MTGC_RG")

def Recieve_from_MTSI():
    RMQ.receive(callback, "", "MTSI_RG")

def Recieve_from_MTPI():
    RMQ.receive(callback, "", "MTPI_RG")

def Recieve_from_RM():
    RMQ.receive(callback, "", "RM_RG")

def Recieve_from_LBHC():
    RMQ.receive(callback, "", "LBHC_RG")

def Recieve_from_LBSI():
    RMQ.receive(callback, "", "LBSI_RG")

def Recieve_from_BS():
    RMQ.receive(callback, "", "BS_RG")

def Recieve_from_HMG():
    RMQ.receive(callback, "", "HM_RGG")

def Recieve_from_HMM():
    RMQ.receive(callback, "", "HM_RGM")

def Recieve_from_HMS():
    RMQ.receive(callback, "", "HM_RGS")

def Recieve_from_HM():
    RMQ.receive(callback, "", "HM_RG")

def Backup():
    Timer = 15
    while 1:
        Registry_obj.Store_DS()
        time.sleep(Timer)

Registry_obj = Registry()

if __name__ == '__main__':

    RMQ = RabbitMQ()

    #REGISTRY <--> DEPLOYMENT MANAGER
    RMQ.create_ServiceQueues("RG", "DM")
    #REGISTRY <--> SERVICE MANAGER
    RMQ.create_ServiceQueues("RG", "SM")
    #REGISTRY <--> MONITOR Host Creds
    RMQ.create_ServiceQueues("RG", "MTHC")
    #REGISTRY <--> MONITOR Gateway Creds
    RMQ.create_ServiceQueues("RG", "MTGC")
    #REGISTRY <--> MONITOR Service Info
    RMQ.create_ServiceQueues("RG", "MTSI")
    #REGISTRY <--> MONITOR Platform Module Info
    RMQ.create_ServiceQueues("RG", "MTPI")
    #REGISTRY <--> RECOVERY MANAGER
    RMQ.create_ServiceQueues("RG", "RM")
    #REGISTRY <--> LOAD BALANCER Host Creds
    RMQ.create_ServiceQueues("RG", "LBHC")
    #REGISTRY <--> LOAD BALANCER Service Inst
    RMQ.create_ServiceQueues("RG", "LBSI")
    #REGISTRY <--> BOOTSTRAPPER
    RMQ.create_ServiceQueues("RG", "BS")
    #REGISTRY <--> Host Manager
    RMQ.create_ServiceQueues("RGM", "HM")
    #REGISTRY <--> Host Manager Gateway link
    RMQ.create_ServiceQueues("RGG", "HM")
    #REGISTRY <--> Host Manager Service inst
    RMQ.create_ServiceQueues("RGS", "HM")

    #REGISTRY <--> Host Manager Service inst
    RMQ.create_ServiceQueues("RG", "HM")

    Registry_obj.Restore_DS()

    # t1 = threading.Thread(target=Recieve_from_SM)
    # t1.start()

    # t2 = threading.Thread(target=Recieve_from_DM)
    # t2.start()

    t3 = threading.Thread(target=Recieve_from_MTHC)
    t3.start()

    t4 = threading.Thread(target=Recieve_from_MTGC)
    t4.start()

    t5 = threading.Thread(target=Recieve_from_MTSI)
    t5.start()

    t6 = threading.Thread(target=Recieve_from_MTPI)
    t6.start()

    # t4 = threading.Thread(target=Recieve_from_RM)
    # t4.start()

    t7 = threading.Thread(target=Recieve_from_LBHC)
    t7.start()

    t8 = threading.Thread(target=Recieve_from_LBSI)
    t8.start()

    # t7 = threading.Thread(target=Recieve_from_BS)
    # t7.start()

    t9 = threading.Thread(target=Backup)
    t9.start()

    t10 = threading.Thread(target=Recieve_from_HMG)
    t10.start()

    t11 = threading.Thread(target=Recieve_from_HMM)
    t11.start()

    t12 = threading.Thread(target=Recieve_from_HMS)
    t12.start()

    t13 = threading.Thread(target=Recieve_from_HM)
    t13.start()
