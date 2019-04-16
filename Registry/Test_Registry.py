from queue_req_resp import RabbitMQ
from Registry_API import Registry_API
import json

Registry_obj = Registry_API("192.168.31.10", 5672 , "harshita", "123")
print("Obj created")

# REQUEST TYPE 1
print("REQUEST TYPE 1")
Registry_obj.Write_Storage_info("234", "/2/34/Models", "/2/34/AppLogic", "/2/34/Services", "/2/34/Config", "RG_DM")
Registry_obj.Write_Storage_info("244", "/2/44/Models", "/2/44/AppLogic", "/2/44/Services", "/2/44/Config", "RG_DM")

# REQUEST TYPE 2
print("REQUEST TYPE 2")
Host_List1 = [ ["192.168.10.23", "6253", "Up"], ["192.163.10.23", "6255", "Down"] ]
Registry_obj.Write_Model_Inst_Info("432", Host_List1, "RG_SM")

Host_List2 = [ ["192.168.10.27", "6298", "Up"], ["192.163.10.25", "6267", "Down"] ]
Registry_obj.Write_Model_Inst_Info("482", Host_List2, "RG_SM")

# REQUEST TYPE 3
print("REQUEST TYPE 3")
Host_List1 = [ ["192.168.10.23", "6253", "Up"], ["192.163.10.23", "6255", "Down"] ]
Registry_obj.Write_Service_Inst_Info("432", Host_List1, "RG_SM")

Host_List2 = [ ["192.168.10.27", "6298", "Up"], ["192.163.10.25", "6267", "Down"] ]
Registry_obj.Write_Service_Inst_Info("482", Host_List2, "RG_SM")

#REQUEST TYPE 4
print("REQUEST TYPE 4")
Host_List1 = [ ["192.168.10.23", "6253", "Up"], ["192.163.10.23", "6255", "Down"] ]
Registry_obj.Write_App_Inst_Info("432", Host_List1, "RG_SM")

Host_List2 = [ ["192.168.10.27", "6298", "Up"], ["192.163.10.25", "6267", "Down"] ]
Registry_obj.Write_App_Inst_Info("482", Host_List2, "RG_SM")

# REQUEST TYPE 5
print("REQUEST TYPE 5")
Registry_obj.Write_Host_Creds("192.168.23.34", "pranjali", "Accio@934", "RG_BS")
Registry_obj.Write_Host_Creds("192.168.23.35", "kratika", "Qwerty987**", "RG_BS")

# REQUEST TYPE 6
print("REQUEST TYPE 6")
Registry_obj.Write_Platform_Module_Info("1", "192.168.23.34", "15329", "192.168.23.35", "15330", "RG_SM")
Registry_obj.Write_Platform_Module_Info("2", "192.168.23.34", "15334", "192.168.23.35", "15335", "RG_SM")

# REQUEST TYPE 7
print("REQUEST TYPE 7")
Registry_obj.Read_Storage_info(["432", "482"], "RG_DM", "DM_RG")

# REQUEST TYPE 8
print("REQUEST TYPE 8")
Registry_obj.Read_App_Inst_Info(["432", "482"], "RG_LB", "LB_RG")

# REQUEST TYPE 9
print("REQUEST TYPE 9")
Registry_obj.Read_Service_Inst_Info(["432", "482"], "RG_LB", "LB_RG")

# REQUEST TYPE 10
print("REQUEST TYPE 10")
Registry_obj.Read_Model_Inst_Info(["432", "482"], "RG_MT", "MT_RG")

# REQUEST TYPE 11
print("REQUEST TYPE 11")
Registry_obj.Read_Host_Creds(["192.168.23.34", "192.168.23.35"], "RG_LB", "LB_RG")

# REQUEST TYPE 12
print("REQUEST TYPE 12")
Registry_obj.Read_Platform_Module_Info(["1", "2"], "RG_RM", "RM_RG")
