import sys
from pathlib import Path
home = str(Path.home())
path = home+'/Platform/'
sys.path.insert (0, path)

import zipfile
import os
from queue_req_resp import RabbitMQ
import json
from nfs_client import NFS
import time
import xml.etree.ElementTree as ET
from lxml import etree
from io import StringIO
import xmlschema
from app import db
from app.models import Service
from sqlalchemy import create_engine 
import shutil

class Deployment_Manager():

    def __init__(self, NFS_Server , Local_Password, Local_mount_relative_path):
       self.NFS_Obj = NFS(NFS_Server, Local_Password)
       self.local_nfs_dir = os.getcwd() + Local_mount_relative_path
       self.Models_Information_To_Return = None
       self.Services_Informtion_To_Return = None

    def Validate_XML(self,XML_Path,Schema_Path):
        my_schema = xmlschema.XMLSchema(Schema_Path)
        try:
            my_schema.is_valid(XML_Path)
            return True
        except:
            print ("Mismatch")
            return False

    # def Parse_Application_config(self,Unzip_Folder_Path):
    #     Application_config_file_path = Unzip_Folder_Path + "/Config/Application_config.xml"


    #     tree = ET.parse(Application_config_file_path)		
    #     root = tree.getroot()
    #     print (root)

    #     # --------------- Service Module ------------------ #

    #     service_data = {}

    #     for children in root.iter('Services'):
    #         for child in children:
    #             attribDictionary = child.attrib
    #             service_name = attribDictionary['name']
    #             service_data[service_name] = {}

    #             for elements in child:
    #                 service_data[service_name][elements.tag] = elements.text

    #     print (service_data)

    #     # ----------- Match service name --------------- #

    #     # for key in service_data.keys():
    #     #     sub_tree = ET.parse(Unzip_Folder_Path + "/Config/"+service_data[key]["DeploymentConfigFile"])		
    #     #     sub_root = sub_tree.getroot()
    #     #     if (sub_root.attrib['name'] != key):
    #     #         return False

    #     # # ----------- Check for "ProductionConfigFile" (used previous for loop) --------------- #

    #     # for key in service_data.keys():
    #     #     sub_tree = ET.parse(service_data[key]["ProductionConfigFile"])		
    #     #     sub_root = sub_tree.getroot()
    #     #     if (sub_root.attrib['name'] != key):
    #     #         return False

    #     # --------------- ApplicationLogic module ------------------ #

    #     App_logic_data = {}

    #     for children in root.iter('ApplicationLogic'):
    #         for child in children:
    #             attribDictionary = child.attrib
    #             App_logic_name = attribDictionary['name']
    #             App_logic_data[App_logic_name] = {}

    #             for elements in child:
    #                 App_logic_data[App_logic_name][elements.tag] = Unzip_Folder_Path + "/Config/"+elements.text

    #     # ----------- Match Config file --------------- #

    #     for key in App_logic_data.keys():
    #         sub_tree = ET.parse(App_logic_data[key]["ConfigFile"])		
    #         sub_root = sub_tree.getroot()
    #         if (sub_root.attrib['name'] != key):
    #             return False
        
    #     return True

    def Get_Models_Or_Services_Information(self, App_Dev_Id, App_Id, Unzip_Folder_Path,Info_To_Fetch): # Info_To_Fetch = "Models" or "Services"
        Application_config_file_path = Unzip_Folder_Path + "/Config/Application_config.xml"

        tree = ET.parse(Application_config_file_path)		
        root = tree.getroot()

        XML_Data = {}

        for children in root.iter(Info_To_Fetch):
            for child in children:
                attribDictionary = child.attrib
                name = attribDictionary['name']
                XML_Data[name] = {}

                for elements in child:
                    XML_Data[name][elements.tag] = Unzip_Folder_Path + "/Config/" + elements.text

        if Info_To_Fetch == "Models":
            self.Models_Information_To_Return = XML_Data
        else:
            self.Services_Informtion_To_Return = XML_Data

        Models_dict = self.Models_Information_To_Return
        Services_dict = self.Services_Informtion_To_Return


        if Info_To_Fetch == "Models":
            for model in Models_dict:
                model_name = model
                model_deploy_config_loc = Models_dict[model_name]['DeploymentConfigFile']
                model_prod_config_loc = Models_dict[model_name]['ProductionConfigFile']
                serv_obj = Service(service_name = model_name , service_type ="model" , app_id = App_Id , deploy_config_loc = model_deploy_config_loc , prod_config_loc = model_prod_config_loc ,service_ui_server="NULL")
                db.session.add(serv_obj)
        else:
            for service in Services_dict:
                service_name = service
                service_deploy_config_loc = Services_dict[service_name]['DeploymentConfigFile']
                service_prod_config_loc = Services_dict[service_name]['ProductionConfigFile']
                serv_obj = Service(service_name = service_name , service_type ="exe" , app_id = App_Id , deploy_config_loc = service_deploy_config_loc , prod_config_loc = service_prod_config_loc ,service_ui_server="NULL")
                db.session.add(serv_obj)

        db.session.commit()
        print("Saved in DB")

        services_dict={}
        #service_name : service_id
        if Info_To_Fetch == "Models":
            for model in  Models_dict:
                model_name=model
                service=Service.query.filter(Service.service_name==model_name).first()
                service_id = service.service_id
                services_dict[model_name]=service_id
        else:
            for service in  Services_dict:
                service_name=service
                serv=Service.query.filter(Service.service_name==service_name).first()
                service_id = serv.service_id
                services_dict[service_name]=service_id

        # print(services_dict)

        Details_of_info_to_fetch = {}

        for key in XML_Data.keys():
            sub_tree = ET.parse(XML_Data[key]["DeploymentConfigFile"])		
            sub_root = sub_tree.getroot()

            Details_of_info_to_fetch[key] = {}

            for elements in sub_root:
                Details_of_info_to_fetch[key][elements.tag] = elements.text


        Final_info_to_fetch = []

        for key in Details_of_info_to_fetch.keys():
            Info = {"Service_ID":None, Info_To_Fetch[:-1]+"_Link":None, "Criticality":None , "No_Instances": None}
            Info["Service_ID"] = str(services_dict[str(key)])
            Info[Info_To_Fetch[:-1]+"_Link"] = "/" + str(App_Dev_Id) + "/" + str(App_Id) + "/"+Info_To_Fetch+"/" + str(key)
            Info["Criticality"] = Details_of_info_to_fetch[key]["Criticality"]
            Info["No_Instances"] = Details_of_info_to_fetch[key]["MinimumInstances"]
            Final_info_to_fetch.append(Info)

        return Final_info_to_fetch


    def Deploy_App(self, App_Dev_Id, App_Id, Package_Absolute_Path):

        # ---------- Unzip Package ------------- #
        Current_Working_Direcory = os.getcwd()

        zip_ref = zipfile.ZipFile(Package_Absolute_Path, 'r')
        zip_ref.extractall(Current_Working_Direcory)
        zip_ref.close()

        Unzip_File_Name = os.path.basename(Package_Absolute_Path)[:-4]

        os.rename(Current_Working_Direcory+"/"+Unzip_File_Name,Current_Working_Direcory+"/"+str(App_Id))


        # --------- check service name ---------- #

        # if(not self.Parse_Application_config(Current_Working_Direcory+"/"+str(App_Id))):
        #     # Send message that service is mismatch #
        #     print ("Mismatch service name")
        #     sys.exit(1)

        # --------- Store in NFS -------------- #

        print ("Connecting to NFS")
        self.NFS_Obj.mount("", self.local_nfs_dir)

        List_Of_Directories = self.NFS_Obj.listdir(self.local_nfs_dir)
        if str(App_Dev_Id) not in List_Of_Directories:
            self.NFS_Obj.mkdir(self.local_nfs_dir+"/"+str(App_Dev_Id))

        self.NFS_Obj.copy(Current_Working_Direcory+"/"+str(App_Id), self.local_nfs_dir+"/"+str(App_Dev_Id)+"/")
        print ("DisConnecting to NFS")
        time.sleep(1)

        self.NFS_Obj.unmount(self.local_nfs_dir)

        # -------------- Artefacts staorage links ------------------- #

        Model_Link = "/"+str(App_Dev_Id)+"/"+str(App_Id)+"/Models"
        App_Link = "/"+str(App_Dev_Id)+"/"+str(App_Id)+"/AppLogic"
        Service_Link = "/"+str(App_Dev_Id)+"/"+str(App_Id)+"/Services"
        Config_Link = "/"+str(App_Dev_Id)+"/"+str(App_Id)+"/Config"
        Models = self.Get_Models_Or_Services_Information(App_Dev_Id, App_Id, Current_Working_Direcory+"/"+str(App_Id),"Models")
        Services = self.Get_Models_Or_Services_Information(App_Dev_Id, App_Id, Current_Working_Direcory+"/"+str(App_Id),"Services")

        print (Models)
        print (Services)
        # print (Model_Link)
        # print (App_Link)
        # print (Service_Link)
        # print (Config_Link)

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
                                "AD_ID" : App_Dev_Id,
                                "App_Id" : App_Id,
                                "Models": Models,
                                "Services" : Services,
                                "App_Link": App_Link,
                                "Config_Link": Config_Link
                                }

        Host_Manager_Message = json.dumps(Host_Manager_Message)
        obj_HM = RabbitMQ()
        obj_HM.send("", "DM_HM", Host_Manager_Message)

        # Deleting temporary folders created
        shutil.rmtree(Current_Working_Direcory+"/"+str(App_Id))
        shutil.rmtree(Current_Working_Direcory+"/nfs_server")




# Sample Function Call
# DM_Obj = Deployment_Manager("10.2.129.68", "S2j1ar1in63", "/nfs_server")
# Models_Info_To_Return, Services_Info_To_Return = DM_Obj.Deploy_App(1,3,"./Application_Developer.zip")
