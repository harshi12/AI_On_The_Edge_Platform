import os
from nfs_client import NFS
import json
from queue_req_resp import RabbitMQ

class Monitor:

    def __init__(self, Local_Password="Accio@934"):
        self.Output_files = {}
        self.Module_Info = {}
        self.Local_Password = Local_Password

    def Read_Module_Info(self, NFS_Server):

        NFS_Path = "/Platform/Modules_Recovery_Info.json"
        local_nfs_dir = os.getcwd() + "/Modules_Recovery_Info"

        nfs_obj = NFS(NFS_Server, self.Local_Password )
        nfs_obj.mount(NFS_Path, local_nfs_dir)

        self.Module_Info = json.loads( open(local_nfs_dir+"/Modules_Recovery_Info.json").read() )
        print(self.Module_Info)

    def Check_Host(self, Module_ID, Host_type):

        Ip = self.Module_Info[Module_ID][Host_type]["IP"]
        Username = self.Module_Info[Module_ID][Host_type]["Username"]
        Password = self.Module_Info[Module_ID][Host_type]["Password"]
        Pid = self.Module_Info[Module_ID][Host_type]["Pid"]

        if os.path.exists("output.txt"):
            os.remove("output.txt")

        # cmd = "echo " + Password + " | ssh " + Username + "@" + Ip + " ps -fp " + str(Pid) + " | wc -l > output.txt --password_stdin"
        cmd = "sshpass -p "+ Password + " ssh " + Username + "@" + Ip + " ps -fp " + str(Pid) + " | wc -l > output.txt"
        print("Command: ", cmd)
        os.system(cmd)

        with open("output.txt") as f:
            content = f.read().strip()
            print("Content: ", content)

        result = int(content)
        return result

    def Check_Status(self):

        for module_id in self.Module_Info.keys():

            pri_result = self.Check_Host(module_id, "Primary")
            print("Primary result: ", pri_result)

            if pri_result == 1:
                rec_result = self.Check_Host(module_id, "Recovery")
                print("Recovery result: ", rec_result)

                if rec_result == 1:
                    print("Both hosts are down. SORRY!")
                else:
                    msg = {"Module_ID" : module_id }
                    json_msg = json.dumps(msg)

                    obj = RabbitMQ()
            		obj.send("", "MT_RM", json_msg)
                    print("Msg sent to Recovery Manager: ", json_msg)
            else:
                print("Primary host is running\n")



M = Monitor()
M.Read_Module_Info("")
M.Check_Status()

#README

# Mount NFS file containing Modeule_ID, Primary (IP, Username, Password, Pid), Secondary (IP, Username, Password, Pid)
# [Run below function for every (Module,Timer) interval]
# Read NFS file and store in local data structure
# Module_ID -> Module_ID.txt mappings
# For each Module (Module, Timer):
    # Check Primary host:
    #1 ssh to Primary IP of module and run ps -fp $pid | wc -l command and write output to Module_ID.txt
    #2 str = Read from Module_ID.txt
    #3 if str == 1 (Primary host is not up)
        # Check Recovery host (1,2,3)
        # If Recovery host is not up : Print FAIL
        # else Send msg to Recovery manager queue [Module_ID]
