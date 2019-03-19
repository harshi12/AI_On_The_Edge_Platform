import queue_req_resp

def Request_Deploy(Receiving_Message, Port):
    IP = Receiving_Message_Json["IPs"]
    Link = Receiving_Message_Json["Link"]
    Docker_Name = Link

    Command = "docker run -t --name " + Docker_Name + " --rm -p " + str(Port) + ":8501 -v /home/ravi/IIIT/SEM2/subjects/IAS/Hackathon2/model:/models/" + Link +" -e MODEL_NAME="+ Link +" tensorflow/serving"
    Command_List = Command.split(" ")
    process = subprocess.Popen(Command_List, stdout=subprocess.PIPE)

    time.sleep(5)

    Docker_Id = os.popen("docker ps -aqf name=\""+Docker_Name+"\"").read()[:-1]
    return Docker_Id,Port

def Request_Kill(Receiving_Message):
    Docker_Id = Receiving_Message_Json["Docker_Id"]
    Dummy_Docker_Id = os.popen("docker kill "+Docker_Id).read()[:-1]

