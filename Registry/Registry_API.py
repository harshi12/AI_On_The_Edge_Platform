from queue_req_resp import RabbitMQ
import json

class Registry_API:

    def __init__(self):
        self.msg_obj = RabbitMQ()

    def Write_Storage_info(self, App_Id, Model_Link, App_Link, Service_Link, Config_Link, Sending_Queue_name):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Write"
        Request_Msg["DS_Name"] = "Storage_info"

        key = "Value"
        if key not in Request_Msg.keys():
            Request_Msg["Value"] = []

        Req_Value = {}
        Req_Value["App_id"] = App_Id
        Req_Value["Model_Link"] = Model_Link
        Req_Value["App_Link"] = App_Link
        Req_Value["Service_Link"] = Service_Link
        Req_Value["Config_Link"] = Config_Link

        Request_Msg["Value"].append(Req_Value)

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Sending_Queue_name, Request_json_msg)
        print("Msg sent: ", Request_json_msg)

    def Write_Service_Link_Info(self, Service_id, Service_link, Sending_Queue_name):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Write"
        Request_Msg["DS_Name"] = "Service_link_info"

        key = "Value"
        if key not in Request_Msg.keys():
            Request_Msg["Value"] = []

        Req_Value = {}
        Req_Value["Service_id"] = Service_id
        Req_Value["Link"] = Service_link

        Request_Msg["Value"].append(Req_Value)

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Sending_Queue_name, Request_json_msg)
        print("Msg sent: ", Request_json_msg)

    def Write_Service_Inst_Info(self, Service_Id, Host_Port_Status_List, Sending_Queue_name):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Write"
        Request_Msg["DS_Name"] = "Service_inst_info"

        key = "Value"
        if key not in Request_Msg.keys():
            Request_Msg["Value"] = []

        Req_Value = {}
        Req_Value["Service_id"] = Service_Id
        Req_Value["Hosts"] = Host_Port_Status_List

        Request_Msg["Value"].append(Req_Value)

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Sending_Queue_name, Request_json_msg)
        print("Msg sent: ", Request_json_msg)

    def Write_App_Inst_Info(self, App_Id, Host_Port_Status_List, Sending_Queue_name):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Write"
        Request_Msg["DS_Name"] = "App_inst_info"

        key = "Value"
        if key not in Request_Msg.keys():
            Request_Msg["Value"] = []

        Req_Value = {}
        Req_Value["App_id"] = App_Id
        Req_Value["Hosts"] = Host_Port_Status_List

        Request_Msg["Value"].append(Req_Value)

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Sending_Queue_name, Request_json_msg)
        print("Msg sent: ", Request_json_msg)

    def Write_Host_Creds(self, Host_IP, Username, Password, Sending_Queue_name):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Write"
        Request_Msg["DS_Name"] = "Host_Creds"

        key = "Value"
        if key not in Request_Msg.keys():
            Request_Msg["Value"] = []

        Req_Value = {}
        Req_Value["Host_IP"] = Host_IP
        Req_Value["Username"] = Username
        Req_Value["Password"] = Password

        Request_Msg["Value"].append(Req_Value)

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Sending_Queue_name, Request_json_msg)
        print("Msg sent: ", Request_json_msg)

    def Write_Gateway_Creds(self, Gateway_IP, Username, Password, Sending_Queue_name):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Write"
        Request_Msg["DS_Name"] = "Host_Creds"

        key = "Value"
        if key not in Request_Msg.keys():
            Request_Msg["Value"] = []

        Req_Value = {}
        Req_Value["Gateway_IP"] = Gateway_IP
        Req_Value["Username"] = Username
        Req_Value["Password"] = Password

        Request_Msg["Value"].append(Req_Value)

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Sending_Queue_name, Request_json_msg)
        print("Msg sent: ", Request_json_msg)

    def Write_Platform_Module_Info(self, Module_id, PrimaryIP, PrimaryPid, RecoveryIP, RecoveryPid, Sending_Queue_name):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Write"
        Request_Msg["DS_Name"] = "Platform_Module_Info"

        key = "Value"
        if key not in Request_Msg.keys():
            Request_Msg["Value"] = []

        Req_Value = {}
        Req_Value["Module_id"] = Module_id
        Req_Value["Primary"] = {}
        Req_Value["Primary"]["IP"] = PrimaryIP
        Req_Value["Primary"]["Pid"] = PrimaryPid
        Req_Value["Recovery"] = {}
        Req_Value["Recovery"]["IP"] = RecoveryIP
        Req_Value["Recovery"]["Pid"] = RecoveryPid

        Request_Msg["Value"].append(Req_Value)

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Sending_Queue_name, Request_json_msg)
        print("Msg sent: ", Request_json_msg)

    def Read_Storage_info(self, App_Id_list, Sending_Queue, Recieving_Queue):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Read"
        Request_Msg["DS_Name"] = "Storage_info"
        Request_Msg["Queue_Name"] = Recieving_Queue

        Request_Msg["Filter"] = {}
        if len(App_Id_list) == 0:
            Request_Msg["Filter"]["App_id"] = []
        else:
            Request_Msg["Filter"]["App_id"] = App_Id_list

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Sending_Queue, Request_json_msg)
        print("Msg sent: ", Request_json_msg)

    def Read_Service_Link_Info(self, Service_Id_list, Sending_Queue, Recieving_Queue):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Read"
        Request_Msg["DS_Name"] = "Service_link_info"
        Request_Msg["Queue_Name"] = Recieving_Queue

        Request_Msg["Filter"] = {}
        if len(Service_Id_list) == 0:
            Request_Msg["Filter"]["Service_id"] = []
        else:
            Request_Msg["Filter"]["Service_id"] = Service_Id_list

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Sending_Queue, Request_json_msg)
        print("Msg sent: ", Request_json_msg)

    def Read_Service_Inst_Info(self, Service_Id_list, Sending_Queue, Recieving_Queue):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Read"
        Request_Msg["DS_Name"] = "Service_inst_info"
        Request_Msg["Queue_Name"] = Recieving_Queue

        Request_Msg["Filter"] = {}
        if len(Service_Id_list) == 0:
            Request_Msg["Filter"]["Service_id"] = []
        else:
            Request_Msg["Filter"]["Service_id"] = Service_Id_list

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Sending_Queue, Request_json_msg)
        print("Msg sent: ", Request_json_msg)

    def Read_App_Inst_Info(self, App_Id_list, Sending_Queue, Recieving_Queue):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Read"
        Request_Msg["DS_Name"] = "App_inst_info"
        Request_Msg["Queue_Name"] = Recieving_Queue

        Request_Msg["Filter"] = {}
        if len(App_Id_list) == 0:
            Request_Msg["Filter"]["App_id"] = []
        else:
            Request_Msg["Filter"]["App_id"] = App_Id_list

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Sending_Queue, Request_json_msg)
        print("Msg sent: ", Request_json_msg)

    def Read_Host_Creds(self, Host_IP_list, Sending_Queue, Recieving_Queue):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Read"
        Request_Msg["DS_Name"] = "Host_Creds"
        Request_Msg["Queue_Name"] = Recieving_Queue

        Request_Msg["Filter"] = {}
        if len(Host_IP_list) == 0:
            Request_Msg["Filter"]["Host_IP"] = []
        else:
            Request_Msg["Filter"]["Host_IP"] = Host_IP_list

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Sending_Queue, Request_json_msg)
        print("Msg sent: ", Request_json_msg)

    def Read_Gateway_Creds(self, Gateway_IP_list, Sending_Queue, Recieving_Queue):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Read"
        Request_Msg["DS_Name"] = "Gateway_Creds"
        Request_Msg["Queue_Name"] = Recieving_Queue

        Request_Msg["Filter"] = {}
        if len(Gateway_IP_list) == 0:
            Request_Msg["Filter"]["Gateway_IP"] = []
        else:
            Request_Msg["Filter"]["Gateway_IP"] = Gateway_IP_list

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Sending_Queue, Request_json_msg)
        print("Msg sent: ", Request_json_msg)

    def Read_Platform_Module_Info(self, Module_id_list, Sending_Queue, Recieving_Queue):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Read"
        Request_Msg["DS_Name"] = "Platform_Module_Info"
        Request_Msg["Queue_Name"] = Recieving_Queue

        Request_Msg["Filter"] = {}
        if len(Module_id_list) == 0:
            Request_Msg["Filter"]["Module_id"] = []
        else:
            Request_Msg["Filter"]["Module_id"] = Module_id_list

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Sending_Queue, Request_json_msg)
        print("Msg sent: ", Request_json_msg)
