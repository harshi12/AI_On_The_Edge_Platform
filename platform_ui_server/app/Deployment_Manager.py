import zipfile
import os
from queue_req_resp import RabbitMQ
import json
from app.nfs_client import NFS
import time

def Deploy(Ad_Id,App_Id,Package_Absolute_Path):

    # ---------- Unzip ------------- #
    Current_Working_Direcory = os.getcwd()

    zip_ref = zipfile.ZipFile(Package_Absolute_Path, 'r')
    zip_ref.extractall(Current_Working_Direcory)
    zip_ref.close()

    Unzip_File_Name = os.path.basename(Package_Absolute_Path)[:-4]

    os.rename(Current_Working_Direcory+"/"+Unzip_File_Name,Current_Working_Direcory+"/"+str(App_Id))

    # --------- Store in NFS -------------- #
    local_nfs_dir = Current_Working_Direcory+"/nfs_mount"
    print ("Connecting to NFS")
    nfs = NFS("192.168.31.29", "bhavi")
    nfs.mount("", local_nfs_dir)

    List_Of_Directories = nfs.listdir(local_nfs_dir)
    if str(Ad_Id) not in List_Of_Directories:
        nfs.mkdir(local_nfs_dir+"/"+str(Ad_Id))

    nfs.copy(Current_Working_Direcory+"/"+str(App_Id), local_nfs_dir+"/"+str(Ad_Id)+"/")
    print ("DisConnecting to NFS")
    time.sleep(5)

    nfs.unmount(local_nfs_dir)

    # -------------- Making 3 Link ------------------- #

    Model_Link = "/"+str(Ad_Id)+"/"+str(App_Id)+"/model"
    App_Link = "/"+str(Ad_Id)+"/"+str(App_Id)+"/App"
    Config_Link = "/"+str(Ad_Id)+"/"+str(App_Id)+"/config"

    print (Model_Link)
    print (App_Link)
    print (Config_Link)

    # ------------- Store in Registry ---------------- #


    Registry_Message = {
                            "Request_Type":"Write","DS_Name":"Storage_info",
                            "Value":
                                [
                                    {
                                        "App_id": App_Id,
                                        "Model_Link": Model_Link,
                                        "App_Link": App_Link,
                                        "Config_Link": Config_Link
                                    }
                                ]
                        }

    Registry_Message = json.dumps(Registry_Message)
    obj_RG = RabbitMQ()
    obj_RG.send("", "DM_RG", Registry_Message)


    # ----------- Send to Host Manager ---------------- #

    Host_Manager_Message = {
	                        "Request_Type": "App_Submit",
                            "AD_ID" : Ad_Id,
                            "App_Id" : App_Id,
                            "Model_Link": Model_Link,
                            "App_Link": App_Link,
                            "Config_Link": Config_Link
                            }

    Host_Manager_Message = json.dumps(Host_Manager_Message)
    obj_HM = RabbitMQ()
    obj_HM.send("", "DM_HM", Host_Manager_Message)
    # # Send_
    # # # Response = Registry_Write()

    # # If(Response):
    # #     Message = {"Request": "App_Submit","Model_link":Model_Link,"App_link":App_Link,"Config_link":Config_Link}
    # #     Message = json.dumps(str(Message))
	# # 	obj = RabbitMQ()
	# # 	obj.send("", "DM_HM", Message)
    return Model_Link , App_Link , Config_Link

#Deploy(5,4,os.getcwd()+"/sonar_application.zip")


# obj = RabbitMQ()
# obj.send("", "DM_RG", Registry_Message)

# nfs = NFS("192.168.2.1", "S2j1ar1in63")
# # nfs.mount('/', "~/nfs_mount")
# # x = nfs.mkdir("~/nfs_mount/ravi")
# List_Of_Directories = nfs.listdir("/home/ravi/nfs_mount/")
# if
# nfs.unmount("/home/ravi/nfs_mount")
# nfs = NFS("192.168.2.1", "S2j1ar1in63")
