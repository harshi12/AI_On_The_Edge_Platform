from queue_req_resp import RabbitMQ
import json
import threading
import sys

RMQ = 0

class Registry:

    def __init__(self):
        self.Storage_info = {}
        self.Model_inst_info = {}
        self.Service_inst_info = {}
        self.App_inst_info = {}

    def Read_DS(self, DS_Name, DS_Obj):
        Result = {}

        if(DS_Name=='Storage_info'):
            Filter = DS_Obj['Filter']['App_id']
            #Filter is a list of App_ids
            for i in range(len(Filter)):
                App_id = Filter[i]
                for key in Storage_info.keys():
                    print("key and app_id: ", key, app_id)
                    if key==App_id:
                        Result[key] = Storage_info[key]
            return Result

        if(DS_Name=='Model_inst_info'):
            Filter = DS_Obj['Filter']['Model_id']
            #Filter is a list of App_ids
            for i in range(len(Filter)):
                Model_id = Filter[i]
                for key in Model_inst_info.keys():
                    print("key and app_id: ", key, Model_id)
                    if key==Model_id:
                        Result[key] = Model_inst_info[key]
            return Result

        if(DS_Name=='Service_inst_info'):
            Filter = DS_Obj['Filter']['Service_id']
            #Filter is a list of App_ids
            for i in range(len(Filter)):
                Service_id = Filter[i]
                for key in Service_inst_info.keys():
                    print("key and Filter_val: ", key, Service_id)
                    if key==Filter_val:
                        Result[key] = Service_inst_info[key]
            return Result

        if(DS_Name=='App_inst_info'):
            Filter = DS_Obj['Filter']['App_id']
            #Filter is a list of App_ids
            for i in range(len(Filter)):
                App_id = Filter[i]
                for key in App_inst_info.keys():
                    print("key and Filter_val: ", key, App_id)
                    if key==Filter_val:
                        Result[key] = App_inst_info[key]
            return Result

    def Write_DS(self, DS_Name, DS_Obj):

        if(DS_Name=='Storage_info'):
            for i in range(len(DS_Obj)):
                #Record is a Dict
                Record = DS_Obj[i]
                App_Id = Record['App_id']

                self.Storage_info[App_Id] = {}

                Model_Link = Record['Model_Link']
                App_Link = Record['App_Link']
                Service_Link = Record['Service_Link']
                Config_Link = Record['Config_Link']

                self.Storage_info[App_Id]['Model_Link'] = Model_Link
                self.Storage_info[App_Id]['App_Link'] = App_Link
                self.Storage_info[App_Id]['Service_Link'] = Service_Link
                self.Storage_info[App_Id]['Config_Link'] = Config_Link

        elif(DS_Name=='Model_inst_info'):
            for i in range(len(DS_Obj)):
                #Record if Dict
                Record = DS_Obj[i]
                Model_Id = Record['Model_id']

                self.Model_inst_info[Model_Id] = []

                for j in range(len(DS_Obj[i]['Hosts'])):
                    Hosts_List = DS_Obj[i]['Hosts']
                    Host_IP = Hosts_List[j][0]
                    Host_Port = Hosts_List[j][1]
                    Model_Status = Hosts_List[j][2]

                    Model_Inst = [Host_IP, Host_Port, Model_Status]
                    self.Model_inst_info[Model_Id].append(Model_Inst)

        elif(DS_Name=='Service_inst_info'):
            for i in range(len(DS_Obj)):
                #Record if Dict
                Record = DS_Obj[i]
                Service_Id = Record['Service_id']

                self.Service_inst_info[Service_Id] = []

                for j in range(len(DS_Obj[i]['Hosts'])):
                    Hosts_List = DS_Obj[i]['Hosts']
                    Host_IP = Hosts_List[j][0]
                    Host_Port = Hosts_List[j][1]
                    Service_Status = Hosts_List[j][2]

                    Service_Inst = [Host_IP, Host_Port, Service_Status]
                    self.Service_inst_info[Service_Id].append(Service_Inst)

        elif(DS_Name=='App_inst_info'):
            for i in range(len(DS_Obj)):
                 #Record if Dict
                 Record = DS_Obj[i]
                 App_Id = Record['App_id']

                 self.App_inst_info[App_Id] = []

                 for j in range(len(DS_Obj[i]['Hosts'])):
                     Hosts_List = DS_Obj[i]['Hosts']
                     Host_IP = Hosts_List[j][0]
                     Host_Port = Hosts_List[j][1]
                     App_Status = Hosts_List[j][2]

                     App_Inst = [Host_IP, Host_Port, App_Status]
                     self.App_inst_info[App_Id].append(App_Inst)
        else :
            print("\nInvalid Data Structure Name\n")

    def Print_DS(self):
        print("\nStorage_info: ", self.Storage_info)
        print("\nModel_inst_info: ", self.Model_inst_info)
        print("\nService_inst_info: ", self.Service_inst_info)
        print("\nApp_inst_info: ", self.App_inst_info)

# Read JSON from common queue , parse it and call Update_DS/Read_DS function
def callback(ch, method, properties, body):

    Registry_obj = Registry()

    global port
    print ("Receiving from Common queue")
    #body = body.decode("utf-8")
    body = body.decode("utf-8").replace('\0', '')

    #Receiving_Message = json.loads(body).replace('\'','\"')
    Receiving_Message = json.loads(body)
    print("\nReceiving_Message: ", Receiving_Message)

    Request_type = Receiving_Message['Request_Type']
    DS_Name = Receiving_Message['DS_Name']

    if(Request_type=='Read'):
        DS_Obj = Receiving_Message['Filter']
        DS_Value = Registry_obj.Read_DS(DS_Name, DS_Obj)
        print("Read content: ", DS_Value)
        #create JSON and send on temp queue

    if(Request_type=='Write'):
        DS_Obj = Receiving_Message['Value']
        Registry_obj.Write_DS(DS_Name, DS_Obj)

    print("\nUpdated Data Structures\n ")
    Registry_obj.Print_DS()


#TEMP queues Ideally, Common queue will be used which will listen from all modules
def Recieve_from_SM():
    # RMQ = RabbitMQ()
    RMQ.receive(callback, "", "SM_RG")

def Recieve_from_DM():
    # RMQ = RabbitMQ()
    RMQ.receive(callback, "", "DM_RG")


if __name__ == '__main__':

    # global RMQ

    IP = sys.argv[1]
    port = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]

    RMQ = RabbitMQ(IP, username, password, port)

    t1 = threading.Thread(target=Recieve_from_SM)
    t1.start()

    t2 = threading.Thread(target=Recieve_from_DM)
    t2.start()
