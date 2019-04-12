from queue_req_resp import RabbitMQ
import json
import threading


class Registry:

    def __init__(self):
        Storage_info = {}
        Service_inst_info = {}
        App_inst_info = {}

    def Read_DS(self, DS_Name):
        pass

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

        elif(DS_Name=='Service_inst_info'):
            for i in range(len(DS_Obj)):
                #Record if Dict
                Record = DS_Obj[i]
                Model_Id = Record['Model_id']

                self.Service_inst_info[Model_Id] = []

                for j in range(len(DS_Obj[i]['Hosts'])):
                    Hosts_List = DS_Obj[i]['Hosts']
                    Host_IP = Hosts_List[j][0]
                    Host_Port = Hosts_List[j][1]
                    Model_Status = Hosts_List[j][2]

                    Model_Inst = [Host_IP, Host_Port, Model_Status]
                    self.Service_inst_info[Model_Id].append(Model_Inst)

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
        DS_Value = Registry_obj.Read_DS(DS_Name)
        #create JSON and send on temp queue

    if(Request_type=='Write'):
        DS_Obj = Receiving_Message['Value']
        Registry_obj.Write_DS(DS_Name, DS_Obj)

    print("\nUpdated Data Structures\n ")
    Registry_obj.Print_DS()

def Recieve_from_SM():
    msg_obj2 = RabbitMQ()
    msg_obj2.receive(callback, "", "SM_RG")

def Recieve_from_DM():
    msg_obj1 = RabbitMQ()
    msg_obj1.receive(callback, "", "DM_RG")

t1 = threading.Thread(target=Recieve_from_SM)
t1.start()

Recieve_from_DM()
