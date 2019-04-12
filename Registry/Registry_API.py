from queue_req_resp import RabbitMQ
import json

class Registry_API:

    def __init__(self, Request_Type, DS_Name):
        self.msg_obj = RabbitMQ()

    def Write_Storage_info(self, App_Id, Model_Link, App_Link, Config_Link, Queue_name):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Write"
        Request_Msg["DS_Name"] = "Storage_info"

        key = "Value"
        if key not in self.Request_Msg.keys():
            Request_Msg["Value"] = []

        Req_Value = {}
        Req_Value["App_Id"] = App_Id
        Req_Value["Model_Link"] = Model_Link
        Req_Value["App_Link"] = App_Link
        Req_Value["Config_Link"] = Config_Link

        Request_Msg.append(Req_Value)

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Queue_name, Request_json_msg)

    def Write_Model_Inst_Info(self, Model_Id, Host_Port_Status_List, Queue_name):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Write"
        Request_Msg["DS_Name"] = "Model_inst_info"

        key = "Value"
        if key not in self.Request_Msg.keys():
            Request_Msg["Value"] = []

        Req_Value = {}
        Req_Value["Model_Id"] = Model_Id
        Req_Value["Hosts"] = Host_Port_Status_List

        Request_Msg.append(Req_Value)

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Queue_name, Request_json_msg)

    def Write_Service_Inst_Info(self, Service_Id, Host_Port_Status_List, Queue_name):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Write"
        Request_Msg["DS_Name"] = "Service_inst_info"

        key = "Value"
        if key not in self.Request_Msg.keys():
            Request_Msg["Value"] = []

        Req_Value = {}
        Req_Value["Service_Id"] = Service_Id
        Req_Value["Hosts"] = Host_Port_Status_List

        Request_Msg.append(Req_Value)

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Queue_name, Request_json_msg)

    def Write_App_Inst_Info(self, App_Id, Host_Port_Status_List, Queue_name):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Write"
        Request_Msg["DS_Name"] = "App_inst_info"

        key = "Value"
        if key not in self.Request_Msg.keys():
            Request_Msg["Value"] = []

        Req_Value = {}
        Req_Value["Service_Id"] = App_Id
        Req_Value["Hosts"] = Host_Port_Status_List

        Request_Msg.append(Req_Value)

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Queue_name, Request_json_msg)

    def Read_Storage_info(self, App_Id_list=[], Queue_name):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Read"
        Request_Msg["DS_Name"] = "Storage_info"

        Req_Value = {}
        if len(App_Id_list) == 0:
            Req_Value["Filter"] = []
        else
            Req_Value["Filter"] = App_Id_list

        Request_Msg.append(Req_Value)

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Queue_name, Request_json_msg)

    def Read_Model_Inst_Info(self, Model_Id_list=[], Queue_name):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Read"
        Request_Msg["DS_Name"] = "Model_Inst_Info"

        Req_Value = {}
        if len(Model_Id_list) == 0:
            Req_Value["Filter"] = []
        else
            Req_Value["Filter"] = Model_Id_list

        Request_Msg.append(Req_Value)

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Queue_name, Request_json_msg)

    def Read_Service_Inst_Info(self, Service_Id_list=[], Queue_name):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Read"
        Request_Msg["DS_Name"] = "Service_Inst_Info"

        Req_Value = {}
        if len(Service_Id_list) == 0:
            Req_Value["Filter"] = []
        else
            Req_Value["Filter"] = Service_Id_list

        Request_Msg.append(Req_Value)

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Queue_name, Request_json_msg)

    def Read_App_Inst_Info(self, App_Id_list=[], Queue_name):

        Request_Msg = {}
        Request_Msg["Request_Type"] = "Read"
        Request_Msg["DS_Name"] = "App_Inst_Info"

        Req_Value = {}
        if len(App_Id_list) == 0:
            Req_Value["Filter"] = []
        else
            Req_Value["Filter"] = App_Id_list

        Request_Msg.append(Req_Value)

        Request_json_msg = json.dumps(Request_Msg)
        self.msg_obj.send("", Queue_name, Request_json_msg)
