import sys
from pathlib import Path
home = str(Path.home())

path = home+'/Platform/'

sys.path.insert (0, path)

import os
from queue_req_resp import RabbitMQ
import json
import threading
import time
from Registry_API import Registry_API

test_obj_DM = {
	"Request_Type": "App_Submit",
	"AD_ID": 2,
	"App_Id": 3,
	"Models": [{
			"Service_ID": "1",
			"Model_Link": "/2/3/Models/sonar",
			"Criticality": "Low",
			"No_Instances": "2"
		},
		{
			"Service_ID": "2",
			"Model_Link": "/2/3/Models/iris",
			"Criticality": "High",
			"No_Instances": "1"
		}
	],
	"Services": [{
			"Service_ID": "1",
			"Service_Link": "/2/3/Services/Distance_alarm",
			"Criticality": "Low",
			"No_Instances": "1"
		},
		{
			"Service_ID": "2",
			"Service_Link": "/2/3/Services/helper",
			"Criticality": "High",
			"No_Instances": "1"
		}
	],
	"App_Link": "/2/3/AppLogic",
	"Config_Link": "/2/3/Config"
}

test_obj_MT1 = {
	"Request_Type": "Model_Submit",
	"Model_ID" : "3",
	"Instances" : "1"
}

#IP_username_password = {"192.168.31.194" : ["sukku", "iforgot"], "192.168.31.38" : ["ravi", "S2j1ar1in63"], "192.168.31.124" : ["kaushik", "rama1729"], "192.168.31.34" : ["kratika", "Qwerty987**"]}
#IP_username_password = {"192.168.31.194" : ["sukku", "iforgot"], "192.168.31.38" : ["ravi", "S2j1ar1in63"]}

class host_manager:
	def __init__(self):
		self.App = {}
		self.Gateway_Creds = {}

	def Read_Gateway_Info(self):
		# Send Read request to registry , response will be in MTHC_RG queue
		rg_obj.Read_Gateway_Creds([], "HM_RG", "RG_HM")
		self.Gateway_Creds = msg_obj.receive_nonblock("", "RG_HM")

	def Service_Deploy(self, IP_username_password, Service_Link):
		Service_ID = self.App["Service_ID"]

		params = Service_Link.split("/")
		self.App["AppDev_ID"] = params[0]
		self.App["App_ID"] = params[1]

		request_msg_service = {}
		request_msg_service["Request_Type"] = "Start_Service"
		request_msg_service["Service_Link"] = []

		IPs = IP_username_password.keys()

		for ip in IPs:
			file = open("NFS_Mount2.sh", "w")
			command = "mkdir -p" + " ~/" + str(self.App["AppDev_ID"]) + "/" + str(self.App["App_ID"]) + "\n"
			command += "echo " + IP_username_password[ip][1] + " | sudo -S apt-get install sshpass\n"
			#command += "sshpass -p \"verma\" ssh red@192.168.31.29 \"exit\"\n"
			command += "sshpass -p \"Akanksha21!\" ssh akanksha@192.168.31.244 \"exit\"\n"
			#command += "echo \"verma\" | sshfs red@192.168.31.29:/Users/red/Documents/nfs_server/" + Service_Link +" ~/" + str(self.App["AppDev_ID"]) + "/" + str(self.App["App_ID"]) + "/Services -o password_stdin"
			#command += "echo \"Akanksha21!\" | sshfs akanksha@10.2.131.55:/mnt/Repository" + Service_Link +" ~" + Service_Link + " -o password_stdin"
			command += "echo \"Akanksha21!\" | sshfs akanksha@192.168.31.244:/mnt/Repository/" + str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"])+" ~/"+  str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"]) +" -o password_stdin"
			file.write(command)
			file.close()
			time.sleep(5)

			os.system("bash transfer_service.sh " +IP_username_password[ip][0] + " " + ip + " " + IP_username_password[ip][1])
			request_msg_service["Service_Link"].append([ip, "~" + Service_Link, Service_ID])
			json_request_msg_service = json.dumps(request_msg_service)
			msg_obj.send("", "HM_SM", json_request_msg_service)
			print("\n\nSent request to SM: ", json_request_msg_service)


	def Model_Deploy(self, IP_username_password, Model_Link):

		Model_ID = self.App["Model_ID"]

		params = Model_Link.split("/")
		self.App["AppDev_ID"] = params[0]
		self.App["App_ID"] = params[1]

		request_msg_model = {}
		request_msg_model["Request_Type"] = "Start_Model"
		request_msg_model["Model_Link"] = []

		IPs = IP_username_password.keys()

		for ip in IPs:
			file = open("NFS_Mount1.sh", "w")
			command = "mkdir -p" + " ~/" + str(self.App["AppDev_ID"]) + "/" + str(self.App["App_ID"]) + "\n"
			command += "echo " + IP_username_password[ip][1] + " | sudo -S apt-get install sshpass\n"
			#command += "sshpass -p \"verma\" ssh red@192.168.31.29 \"exit\"\n"
			command += "sshpass -p \"Akanksha21!\" ssh akanksha@192.168.31.244 \"exit\"\n"
			#command += "echo \"verma\" | sshfs red@192.168.31.29:/Users/red/Documents/nfs_server" + Model_Link +" ~"+ Model_Link +" -o password_stdin"
			#command += "echo \"Akanksha21!\" | sshfs akanksha@10.2.131.55:/mnt/Repository" + Model_Link +" ~"+ Model_Link +" -o password_stdin"
			command += "echo \"Akanksha21!\" | sshfs akanksha@192.168.31.244:/mnt/Repository/" + str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"])+" ~/"+  str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"]) +" -o password_stdin"
			file.write(command)
			file.close()
			time.sleep(5)

			os.system("bash transfer_model.sh " +IP_username_password[ip][0] + " " + ip + " " + IP_username_password[ip][1])
			request_msg_model["Model_Link"].append([ip, "~" + Model_Link, Model_ID])

		json_request_msg_model = json.dumps(request_msg_model)
		msg_obj.send("", "HM_SM", json_request_msg_model)
		print("\n\nSent request to SM: ", json_request_msg_model)


	def Host_Deploy(self, IP_username_password):

		request_msg_model = {}
		request_msg_model["Request_Type"] = "Start_Model"
		request_msg_model["Model_Link"] = []

		request_msg_app = {}
		request_msg_app["Request_Type"] = "Start_App"
		request_msg_app["App_Link"] = []

		request_msg_service = {}
		request_msg_service["Request_Type"] = "Start_Service"
		request_msg_service["Service_Link"] = []


		IPs = list(IP_username_password)
		print("Ips from load balancer:", IPs)
		j = 0

		Models = self.App["Models"]
		for model in Models:
			if model["Criticality"] == "No":
				Model_Link = model["Model_Link"]
				No_Instances = int(model["No_Instances"])
				print("\nMODEL BEING INSTALLED: " + Model_Link + " INSTANCES:" + str(No_Instances))
				for i in range(No_Instances):
					file = open("NFS_Mount1.sh", "w")
					command = "mkdir -p" + " ~/" + str(self.App["AppDev_ID"]) + "/" + str(self.App["App_ID"]) + "\n"
					command += "echo " + IP_username_password[IPs[j]][1] + " | sudo -S apt-get install sshpass\n"
					#command += "sshpass -p \"verma\" ssh red@192.168.31.29 \"exit\"\n"
					command += "sshpass -p \"Akanksha21!\" ssh akanksha@192.168.31.244 \"exit\"\n"
					#command += "echo \"verma\" | sshfs red@192.168.31.29:/Users/red/Documents/nfs_server" + Model_Link +" ~"+ Model_Link +" -o password_stdin"
					#command += "echo \"Akanksha21!\" | sshfs akanksha@10.2.131.55:/mnt/Repository" + Model_Link +" ~"+ Model_Link +" -o password_stdin"
					command += "echo \"Akanksha21!\" | sshfs akanksha@192.168.31.244:/mnt/Repository/" + str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"])+" ~/"+  str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"]) +" -o password_stdin"
					file.write(command)
					file.close()
					time.sleep(5)

					os.system("bash transfer_model.sh " +IP_username_password[IPs[j]][0] + " " + IPs[j] + " " + IP_username_password[IPs[j]][1])
					request_msg_model["Model_Link"].append([IPs[j], "~" + Model_Link, model["Service_ID"]])
					j = j + 1

		Services = self.App["Services"]
		for service in Services:
			if service["Criticality"] == "No":
				Service_Link = service["Service_Link"]
				No_Instances = int(service["No_Instances"])
				print("\nSERVICE BEING INSTALLED: " + Service_Link + " INSTANCES:" + str(No_Instances))
				for i in range(No_Instances):
					file = open("NFS_Mount2.sh", "w")
					command = "mkdir -p" + " ~/" + str(self.App["AppDev_ID"]) + "/" + str(self.App["App_ID"]) + "\n"
					command += "echo " + IP_username_password[IPs[j]][1] + " | sudo -S apt-get install sshpass\n"
					#command += "sshpass -p \"verma\" ssh red@192.168.31.29 \"exit\"\n"
					command += "sshpass -p \"Akanksha21!\" ssh akanksha@192.168.31.244 \"exit\"\n"
					#command += "echo \"verma\" | sshfs red@192.168.31.29:/Users/red/Documents/nfs_server/" + Service_Link +" ~/" + str(self.App["AppDev_ID"]) + "/" + str(self.App["App_ID"]) + "/Services -o password_stdin"
					#command += "echo \"Akanksha21!\" | sshfs akanksha@10.2.131.55:/mnt/Repository" + Service_Link +" ~" + Service_Link + " -o password_stdin"
					command += "echo \"Akanksha21!\" | sshfs akanksha@192.168.31.244:/mnt/Repository/" + str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"])+" ~/"+  str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"]) +" -o password_stdin"
					file.write(command)
					file.close()
					time.sleep(5)

					os.system("bash transfer_service.sh " +IP_username_password[IPs[j]][0] + " " + IPs[j] + " " + IP_username_password[IPs[j]][1])
					request_msg_service["Service_Link"].append([IPs[j], "~" + Service_Link, service["Service_ID"]])
					j = j + 1


		App_Link = self.App["App_Link"]
		print("\nAPP BEING INSTALLED:", App_Link)
		file = open("NFS_Mount3.sh", "w")
		command = "mkdir -p ~/" + str(self.App["AppDev_ID"]) + "/" + str(self.App["App_ID"]) + "\n"
		command += "echo " + IP_username_password[IPs[j]][1] + " | sudo -S apt-get install sshpass\n"
		#command += "sshpass -p \"verma\" ssh red@192.168.31.29 \"exit\"\n"
		command += "sshpass -p \"Akanksha21!\" ssh akanksha@192.168.31.244 \"exit\"\n"
		#command += "echo \"verma\" | sshfs red@192.168.31.29:/Users/red/Documents/nfs_server/" + str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"])+"/AppLogic ~"+ App_Link +" -o password_stdin"
		command += "echo \"Akanksha21!\" | sshfs akanksha@192.168.31.244:/mnt/Repository/" + str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"])+" ~/"+  str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"]) +" -o password_stdin"
		file.write(command)
		file.close()
		time.sleep(5)

		os.system("bash transfer_app.sh " +IP_username_password[IPs[j]][0] + " " + IPs[j] + " " + IP_username_password[IPs[j]][1])
		request_msg_app["App_Link"].append([IPs[j], "~" + App_Link + "/UI"])

		json_request_msg_model = json.dumps(request_msg_model)
		json_request_msg_app = json.dumps(request_msg_app)
		json_request_msg_service = json.dumps(request_msg_service)

		msg_obj.send("", "HM_SM", json_request_msg_model)
		print("\n\nSent request to SM: ", json_request_msg_model)
		time.sleep(5)
		msg_obj.send("", "HM_SM", json_request_msg_app)
		print("\n\nSent request to SM: ", json_request_msg_app)
		time.sleep(5)
		msg_obj.send("", "HM_SM", json_request_msg_service)
		print("\n\nSent request to SM: ", json_request_msg_service)

	def Gateway_Deploy(self, Model_Link):
		IPs = self.App["IPs"]
		Service_ID = self.App["Service_ID"]

		params = Model_Link.split("/")
		self.App["AppDev_ID"] = params[0]
		self.App["App_ID"] = params[1]

		request_msg_model = {}
		request_msg_model["Request_Type"] = "Start_Model"
		request_msg_model["Model_Link"] = []

		for ip in IPs:
			file = open("NFS_Mount.sh", "w")
			command = "mkdir -p" + " ~/" + str(self.App["AppDev_ID"]) + "/" + str(self.App["App_ID"]) + "\n"
			command += "echo " + self.Gateway_Creds[ip]["Password"] + " | sudo -S apt-get install sshpass\n"
			#command += "sshpass -p \"verma\" ssh red@192.168.31.29 \"exit\"\n"
			command += "sshpass -p \"Akanksha21!\" ssh akanksha@192.168.31.244 \"exit\"\n"
			#command += "echo \"verma\" | sshfs red@192.168.31.29:/Users/red/Documents/nfs_server" + Model_Link + " ~"+ Model_Link + " -o password_stdin"
			#command += "echo \"Akanksha21!\" | sshfs akanksha@10.2.131.55:/mnt/Repository" + Model_Link +" ~"+ Model_Link +" -o password_stdin"
			command += "echo \"Akanksha21!\" | sshfs akanksha@192.168.31.244:/mnt/Repository/" + str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"])+" ~/"+  str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"]) +" -o password_stdin"
			file.write(command)
			file.close()
			time.sleep(5)

			os.system("bash transfer_model.sh " +self.Gateway_Creds[ip]["Username"] + " " + ip + " " + self.Gateway_Creds[ip]["Password"])
			#os.system('echo %s | sudo -S %s' % ("verma", command))
			request_msg_model["Model_Link"].append([ip, "~" + Model_Link, Service_ID])
		json_request_msg_model = json.dumps(request_msg_model)

		msg_obj.send("", "HM_SM", json_request_msg_model)
		print("\n\nSent request to SM: ", json_request_msg_model)

# def callback_LB(ch, method, properties, body):
# 	print("Receiving IPs from Load Balancer")
# 	Receiving_Message = json.loads(body)
# 	# Load Balancer gives unique IPs ALWAYS!!!!
# 	hm_obj.Host_Deploy(Receiving_Message)


# def callback_RGM(ch, method, properties, body):
# 	print("Receiving Model Links from Registry")
# 	Receiving_Message = json.loads(body)
# 	hm_obj.Model_Deploy(hm_obj.App["IPs"], Receiving_Message[hm_obj.App["Model_ID"]])

# def callback_LBM(ch, method, properties, body):
# 	print("Receiving IPs from Load Balancer")
# 	Receiving_Message = json.loads(body)
# 	hm_obj.App["IPs"] = Receiving_Message
# 	# Load Balancer gives unique IPs ALWAYS!!!!
# 	Service_ID = hm_obj.App["Model_ID"]
# 	rg_obj.Read_Service_Link_Info([Service_ID], "HM_RGM", "RGM_HM")
# 	# msg_obj.receive(callback_RGM, "", "RG_HM")

# def callback_RGS(ch, method, properties, body):
# 	print("Receiving Service Links from Registry")
# 	Receiving_Message = json.loads(body)
# 	hm_obj.Service_Deploy(hm_obj.App["IPs"], Receiving_Message[hm_obj.App["Service_ID"]])
# 	print("SERVICE DEPLOYED FROM MONITOR")

# def callback_LBS(ch, method, properties, body):
# 	print("Receiving IPs from Load Balancer")
# 	Receiving_Message = json.loads(body)
# 	hm_obj.App["IPs"] = Receiving_Message
# 	# Load Balancer gives unique IPs ALWAYS!!!!
# 	Service_ID = hm_obj.App["Service_ID"]
# 	rg_obj.Read_Service_Link_Info([Service_ID], "HM_RGS", "RGS_HM")
# 	print("Sent to RG queue")
# 	# msg_obj.receive(callback_RGS, "", "RG_HM")

# def callback_RGG(ch, method, properties, body):
# 	print("Receiving Service Links from Registry")
# 	Receiving_Message = json.loads(body)
# 	hm_obj.Gateway_Deploy(Receiving_Message[hm_obj.App["Service_ID"]])


def callback_DM(ch, method, properties, body):
	global port
	print ("Receiving links from Deployment Manager")

	Receiving_Message = json.loads(body)
	Request_Type = Receiving_Message["Request_Type"]

	if Request_Type == "Service_Submit":
		hm_obj.App["Service_ID"] = Receiving_Message["Service_ID"]
		hm_obj.App["Instances"] = Receiving_Message["Instances"]

		print("Request: Service Submit")
		print("Service ID:", hm_obj.App["Service_ID"])

		req_obj_LB = {}
		req_obj_LB["Type"] = "Host"
		req_obj_LB["Number"] = str(hm_obj.App["Instances"])
		req_obj_LB_json = json.dumps(req_obj_LB)
		msg_obj.send("", "HM_LB", req_obj_LB_json)
		# msg_obj.receive(callback_LBS, "", "LB_HM")
		print("Receiving IPs from Load Balancer")
		Receiving_Message = msg_obj.receive_nonblock("", "LB_HM")
		Receiving_Message = json.loads(Receiving_Message)
		hm_obj.App["IPs"] = Receiving_Message
		# Load Balancer gives unique IPs ALWAYS!!!!
		Service_ID = hm_obj.App["Service_ID"]
		rg_obj.Read_Service_Link_Info([Service_ID], "HM_RG", "RG_HM")
		print("Sent to RG queue")
		Receiving_Message = msg_obj.receive_nonblock("", "RG_HM")
		# msg_obj.receive(callback_RGS, "", "RG_HM")
		print("Receiving Service Links from Registry")
		Receiving_Message = json.loads(Receiving_Message)
		hm_obj.Service_Deploy(hm_obj.App["IPs"], Receiving_Message[hm_obj.App["Service_ID"]])
		print("SERVICE DEPLOYED FROM MONITOR")

	if Request_Type == "Model_Submit":
		hm_obj.App["Model_ID"] = Receiving_Message["Model_ID"]
		hm_obj.App["Instances"] = Receiving_Message["Instances"]

		print("Request: Model Submit")
		print("Model ID:", hm_obj.App["Model_ID"])

		req_obj_LB = {}
		req_obj_LB["Type"] = "Host"
		req_obj_LB["Number"] = str(hm_obj.App["Instances"])
		req_obj_LB_json = json.dumps(req_obj_LB)
		msg_obj.send("", "HM_LB", req_obj_LB_json)
		Receiving_Message = msg_obj.receive_nonblock("", "LB_HM")
		# msg_obj.receive(callback_LBM, "", "LB_HM")
		print("Receiving IPs from Load Balancer")
		Receiving_Message = json.loads(Receiving_Message)
		hm_obj.App["IPs"] = Receiving_Message
		# Load Balancer gives unique IPs ALWAYS!!!!
		Service_ID = hm_obj.App["Model_ID"]
		rg_obj.Read_Service_Link_Info([Service_ID], "HM_RG", "RG_HM")
		Receiving_Message = msg_obj.receive_nonblock("", "RG_HM")
		# msg_obj.receive(callback_RGM, "", "RG_HM")
		print("Receiving Model Links from Registry")
		Receiving_Message = json.loads(Receiving_Message)
		hm_obj.Model_Deploy(hm_obj.App["IPs"], Receiving_Message[hm_obj.App["Model_ID"]])

	if(Request_Type == "App_Submit"):
		hm_obj.App["Models"] = Receiving_Message["Models"]
		hm_obj.App["App_Link"] = Receiving_Message["App_Link"]
		hm_obj.App["Config_Link"] = Receiving_Message["Config_Link"]
		hm_obj.App["AppDev_ID"] = Receiving_Message["AD_ID"]
		hm_obj.App["App_ID"] = Receiving_Message["App_Id"]
		hm_obj.App["Services"] = Receiving_Message["Services"]

		print("Models:", hm_obj.App["Models"])
		print("Services:", hm_obj.App["Services"])
		print("App Logic:", hm_obj.App["App_Link"])
		print("App ID:", hm_obj.App["App_ID"])
		print("Application ID:", hm_obj.App["AppDev_ID"])

		req_obj_LB = {}
		Instances = 1

		Models = hm_obj.App["Models"]
		for model in Models:
			if model["Criticality"] == "No":
				Instances += int(model["No_Instances"])
		Services = hm_obj.App["Services"]
		for service in Services:
			if service["Criticality"] == "No":
				Instances += int(service["No_Instances"])

		req_obj_LB["Type"] = "Host"
		req_obj_LB["Number"] = str(Instances)
		req_obj_LB_json = json.dumps(req_obj_LB)
		msg_obj.send("", "HM_LB", req_obj_LB_json)
		print("Receiving IPs from Load Balancer")
		Receiving_Message = msg_obj.receive_nonblock("", "LB_HM")
		Receiving_Message = json.loads(body)
		# Load Balancer gives unique IPs ALWAYS!!!!
		hm_obj.Host_Deploy(Receiving_Message)
		# msg_obj.receive(callback_LB, "", "LB_HM")

	if(Request_Type == "Gateway_Deploy"):
		hm_obj.App["Service_ID"] = Receiving_Message["Service_ID"]
		hm_obj.App["IPs"] = Receiving_Message["Gateway_IPs"]

		print("GATEWAY REQUEST\n")

		Service_ID = hm_obj.App["Service_ID"]
		rg_obj.Read_Service_Link_Info([Service_ID], "HM_RG", "RG_HM")
		#msg_obj.receive(callback_RGG, "", "RG_HM")
		Receiving_Message = msg_obj.receive_nonblock("", "RG_HM")
		print("Receiving Service Links from Registry")
		Receiving_Message = json.loads(body)
		hm_obj.Gateway_Deploy(Receiving_Message[hm_obj.App["Service_ID"]])


def listen_DM():

	#Receive Application info from Deployment Manager
	msg_obj.receive(callback_DM, "", "DM_HM")


def listen_MT():

	msg_obj.receive(callback_DM, "", "MT_HM")


def listen_LB():
	msg_obj.receive(callback_DM, "", "LBB_HM")

def listen_LB():
	msg_obj.receive(callback_DM, "", "FM_HM")

msg_obj = RabbitMQ()
hm_obj = host_manager()
rg_obj = Registry_API()

msg_obj.create_ServiceQueues("DM", "RG")
msg_obj.create_ServiceQueues("MT", "HM")
msg_obj.create_ServiceQueues("SM", "RG")
msg_obj.create_ServiceQueues("DM", "HM")
msg_obj.create_ServiceQueues("RG", "HM")
msg_obj.create_ServiceQueues("LBB", "HM")

msg_obj.create_ServiceQueues("LB", "HM")

# t0 = threading.Thread(target = listen_RG)
t1 = threading.Thread(target = listen_DM)
t2 = threading.Thread(target = listen_MT)
t6 = threading.Thread(target = listen_LB)
t7 = threading.Thread(target = listen_FM)


# t0.start()
hm_obj.Read_Gateway_Info()

t1.start()
t2.start()
t6.start()
t7.start()


# #TESTING
# test_obj = json.dumps(test_obj)
# callback_DM(1, 2, 3, test_obj)
