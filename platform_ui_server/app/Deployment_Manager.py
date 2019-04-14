import zipfile
import os
from queue_req_resp import RabbitMQ
import json
from app.nfs_client import NFS
import time

class Deployment_Manager():

    def __init__(self, NFS_Server="192.168.31.29", Local_Password="iforgot", Local_mount_relative_path = "/nfs_mount"):
       self.NFS_Obj = NFS(NFS_Server, Local_Password)
       self.local_nfs_dir = os.getcwd() + Local_mount_relative_path

    def Deploy_App(self, App_Dev_Id, App_Id, Package_Absolute_Path):

        # ---------- Unzip Package ------------- #
        Current_Working_Direcory = os.getcwd()

        zip_ref = zipfile.ZipFile(Package_Absolute_Path, 'r')
        zip_ref.extractall(Current_Working_Direcory)
        zip_ref.close()

        Unzip_File_Name = os.path.basename(Package_Absolute_Path)[:-4]

        os.rename(Current_Working_Direcory+"/"+Unzip_File_Name,Current_Working_Direcory+"/"+str(App_Id))

        # --------- Store in NFS -------------- #
        print ("Connecting to NFS")
        self.NFS_Obj.mount("", self.local_nfs_dir)

        List_Of_Directories = self.NFS_Obj.listdir(self.local_nfs_dir)
        if str(App_Dev_Id) not in List_Of_Directories:
            self.NFS_Obj.mkdir(self.local_nfs_dir+"/"+str(App_Dev_Id))

        self.NFS_Obj.copy(Current_Working_Direcory+"/"+str(App_Id), self.local_nfs_dir+"/"+str(App_Dev_Id)+"/")
        print ("DisConnecting to NFS")
        time.sleep(5)

        self.NFS_Obj.unmount(self.local_nfs_dir)

        # -------------- Artefacts staorage links ------------------- #

        Model_Link = "/"+str(Ad_Id)+"/"+str(App_Id)+"/Models"
        App_Link = "/"+str(Ad_Id)+"/"+str(App_Id)+"/AppLogic"
        Service_Link = "/"+str(Ad_Id)+"/"+str(App_Id)+"/Services"
        Config_Link = "/"+str(Ad_Id)+"/"+str(App_Id)+"/Config"

        print (Model_Link)
        print (App_Link)
        print (Service_Link)
        print (Config_Link)

        # ------------- Store Artefacts staorage links in Registry ---------------- #

        Registry_Message = {
                                "Request_Type":"Write",
                                "DS_Name":"Storage_info",
                                "Value":
                                    [
                                        {
                                            "App_id": App_Id,
                                            "Model_Link": Model_Link,
                                            "App_Link": App_Link,
                                            "Service_Link" : Service_Link,
                                            "Config_Link": Config_Link
                                        }
                                    ]
                            }

        Registry_Message = json.dumps(Registry_Message)
        obj_RG = RabbitMQ()
        obj_RG.send("", "DM_RG", Registry_Message)

        # ----------- Send request to Host Manager ---------------- #

        Host_Manager_Message = {
    	                        "Request_Type": "App_Submit",
                                "AD_ID" : Ad_Id,
                                "App_Id" : App_Id,
                                "Model_Link": Model_Link,
                                "App_Link": App_Link,
                                "Service_Link" : Service_Link,
                                "Config_Link": Config_Link
                                }

        Host_Manager_Message = json.dumps(Host_Manager_Message)
        obj_HM = RabbitMQ()
        obj_HM.send("", "DM_HM", Host_Manager_Message)

        return Model_Link , App_Link , Config_Link

# Sample Function Call
# DM_Obj = Deployment_Manager("192.168.31.29", "iforgot", "/nfs_mount")
# DM_Obj.Deploy_App(1,2,"/Users/pranjali/Desktop/IAS.zip")