from queue_req_resp import RabbitMQ
from threading import Thread
import requests
import json
import os
import time
import sys
import subprocess
import signal

################# DM Data Structures #################################
portBegin = 8501
threadService = {} #MAP that will store modelID : threadID so that thread can be deleted
hostOccupiedPorts = {} #MAP that will store hostIP : [occupied ports list]
IP_username_password = {"192.168.31.194" : ["sukku", "iforgot"], "192.168.31.38" : ["ravi", "S2j1ar1in63"], "192.168.43.76" : ["bhavidhingra", "bhavi"], "192.168.31.10" : ["harshita", "@14799741hA"], "192.168.31.34" : ["kratika", "Qwerty987**"], "192.168.31.124" : ['hitesh', 'rama1729']}
################# DM Data Structures #################################

RMQ = None


class serviceManager():
	def __init__(self):
		RMQ.create_ServiceQueues("SM","HM") #queue between service manager and host manager
		RMQ.create_queue("","SM_TM") #queue between service manager and topology manager
		RMQ.create_queue("", "Registry_SM") #queue between SM and registry where registry will write
		RMQ.create_queue("", "Inference_SM")
		t1 = Thread(target = self.receiveInputSM, args = ('', "HM_SM")) #thread that will monitor HM_SM Queue	
		t2 = Thread(target = self.receiveInferenceInput, args = ('', "Inference_SM")) #thread that will monitor HM_SM Queue	
		t2.start()
		t1.start()

	# Function that will monitor DM_SM Queue - to receive startService from Inferencing common queue
	def receiveInferenceInput(self, exchange, key):
		RMQ.receive(self.processInferenceInput, exchange, key)

	def processInferenceInput(self, ch, method, properties, body):
		pass

	# Function that will monitor DM_SM Queue - to receive startService from DM
	def receiveInputSM(self, exchange, key):
		RMQ.receive(self.processInputSM, exchange, key)

	def processInputSM(self, ch, method, properties, body):
		data = json.loads(body)
		requestType = data['Request_Type']
		global hostOccupiedPorts
		global threadService
		if requestType == 'Start_Model': # AI model
			print("Received a request to start a service from Host Manager")
			hostList = data['Hosts']
			serviceID = data['Service_ID']

			for IP in hostList:
				new_port = 0
				if IP in hostOccupiedPorts:
					new_port = hostOccupiedPorts[IP][-1] + 1 #increase port_numbers by 1
				else:
					new_port = portBegin

				servicePath = "\"/home/"+str(IP_username_password[IP][0])+"/"+str(serviceID)+"/Models/sonar_model/\""
				print("servicePath:", servicePath)
				commandStr = "tensorflow_model_server --rest_api_port=" + str(new_port) + " --model_name=" + str(serviceID) + " --model_base_path=" + servicePath 
				print("commandStr", commandStr)

				osCommand = "sshpass -p \'" + IP_username_password[IP][1] + "\' ssh -o StrictHostKeyChecking=no -t " + IP_username_password[IP][0] + "@" + IP +" \'" +commandStr +"\'"
				print("osCommand: ", osCommand)
				
				t5 = Thread(target = self.startServing, args = (osCommand,serviceID, IP, new_port))
				# os.system(osCommand)
				t5.start()

				if serviceID not in threadService:
					threadService[serviceID] = [t5]
				else:
					threadService[serviceID].append(t5)

				print("TF serving successfully started for service id:", serviceID," on host:", IP,":",new_port)

				if IP not in hostOccupiedPorts:
					hostOccupiedPorts[IP] = [new_port]
				else:
					hostOccupiedPorts[IP].append(new_port)

		elif requestType == 'Start_App': #flask application
			print("Start_App request")

		elif requestType == 'Start_Service': # non AI services
			print("Start_Service request")


	def startServing(self, osCommand, serviceID, IP, port):
		global hostOccupiedPorts
		# pro = subprocess.Popen(osCommand, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
		# toRegistry = {"Request_Type" : "Write", "DS_Name" : "Service_inst_info", "Value" : [{}]}


		os.system(osCommand)

		# time.sleep(50)
		# os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
		# print("Killed the tensorflow serving for:", IP,":", port)
		# runningServiceList = hostOccupiedPorts[IP]
		# runningServiceList.remove(port)
		# hostOccupiedPorts[IP] = runningServiceList
		#threadService[serviceID].remove() #--> remove the thread id stored in the map
		return

if __name__ == '__main__':
	RMQ = RabbitMQ()

	SM = serviceManager()

'''
{
"Request_Type" : "Start_Model"
"Service_ID" : 2
"Hosts" : ["1.2.3.4", "22.44.2.6"]
}

{
"Request_Type" : "Start_App"
"Service_ID" : 2
"Hosts" : ["1.2.3.4", "22.44.2.6"]
}

{
"Request_Type" : "Start_Service"
"Service_ID" : 2
"Hosts" : ["1.2.3.4", "22.44.2.6"]
}
'''