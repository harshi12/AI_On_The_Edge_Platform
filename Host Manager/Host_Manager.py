import os
from queue_req_resp import RabbitMQ
import json
import threading 
import time

test_obj_DM = {
	"Request_Type": "App_Submit",
	"AD_ID": 2,
	"App_Id": 3,
	"Models": [{
			"Model_Link": "/2/3/Models/sonar",
			"Criticality": "Low",
			"No_Instances": "2"
		},
		{
			"Model_Link": "/2/3/Models/iris",
			"Criticality": "High",
			"No_Instances": "1"
		}
	],
	"Services": [{
			"Service_Link": "/2/3/Services/Distance_alarm",
			"Criticality": "Low",
			"No_Instances": "1"
		},
		{
			"Service_Link": "/2/3/Services/helper",
			"Criticality": "High",
			"No_Instances": "1"
		}
	],
	"App_Link": "/2/3/AppLogic",
	"Config_Link": "/2/3/Config"
}

test_obj_FM = {
	"Request_Type": "Gateway_Deploy",
	"AD_ID": 2,
	"App_ID": 3,
	"Model_Link": "/2/3/Models",
	"Gateway_IPs": ["192,168.31.38", "192.168.31.11"]
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

	def Service_Deploy(self, IP_username_password):
		Service_Link = self.App["Service_ID"]
		params = Service_Link.split("/")
		self.App["AppDev_ID"] = params[0]
		self.App["App_ID"] = params[1]

		request_msg_service = {}
		request_msg_service["Request_Type"] = "Start_Service"
		request_msg_service["Service_Link"] = []

		IPs = self.IP_username_password.keys()

		for ip in IPs:
			file = open("NFS_Mount2.sh", "w")
			command = "mkdir -p ~" + Service_Link + "\n"
			command += "echo " + IP_username_password[ip][1] + " | sudo -S apt-get install sshpass\n"
			#command += "sshpass -p \"verma\" ssh red@192.168.31.29 \"exit\"\n"
			command += "sshpass -p \"Akanksha21!\" ssh akanksha@192.168.31.244 \"exit\"\n"
			#command += "echo \"verma\" | sshfs red@192.168.31.29:/Users/red/Documents/nfs_server/" + Service_Link +" ~/" + str(self.App["AppDev_ID"]) + "/" + str(self.App["App_ID"]) + "/Services -o password_stdin"
			command += "echo \"Akanksha21!\" | sshfs akanksha@192.168.31.244:/mnt/Repository" + Service_Link +" ~" + Service_Link + " -o password_stdin"
			file.write(command)
			file.close()
			time.sleep(5)

			os.system("bash transfer_service.sh " +IP_username_password[ip][0] + " " + ip + " " + IP_username_password[ip][1])
			request_msg_service["Service_Link"].append([ip, "~" + Service_Link])


	def Model_Deploy(self, IP_username_password):

		Model_Link = self.App["Model_ID"]
		params = Model_Link.split("/")
		self.App["AppDev_ID"] = params[0]
		self.App["App_ID"] = params[1]

		request_msg_model = {}
		request_msg_model["Request_Type"] = "Start_Model"
		request_msg_model["Model_Link"] = []

		IPs = IP_username_password.keys()

		for ip in IPs:
			file = open("NFS_Mount1.sh", "w")
			command = "mkdir -p ~" + Model_Link + "\n"
			command += "echo " + IP_username_password[ip][1] + " | sudo -S apt-get install sshpass\n"
			#command += "sshpass -p \"verma\" ssh red@192.168.31.29 \"exit\"\n"
			command += "sshpass -p \"Akanksha21!\" ssh akanksha@192.168.31.244 \"exit\"\n"
			#command += "echo \"verma\" | sshfs red@192.168.31.29:/Users/red/Documents/nfs_server" + Model_Link +" ~"+ Model_Link +" -o password_stdin"
			command += "echo \"Akanksha21!\" | sshfs akanksha@192.168.31.244:/mnt/Repository" + Model_Link +" ~"+ Model_Link +" -o password_stdin"
			file.write(command)
			file.close()
			time.sleep(5)

			os.system("bash transfer_model.sh " +IP_username_password[ip][0] + " " + ip + " " + IP_username_password[ip][1])
			request_msg_model["Model_Link"].append([ip, "~" + Model_Link])

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
			if model["Criticality"] == "Low":
				Model_Link = model["Model_Link"]
				No_Instances = int(model["No_Instances"])
				print("\nMODEL BEING INSTALLED: " + Model_Link + " INSTANCES:" + str(No_Instances))
				for i in range(No_Instances):
					file = open("NFS_Mount1.sh", "w")
					command = "mkdir -p ~" + Model_Link + "\n"
					command += "echo " + IP_username_password[IPs[j]][1] + " | sudo -S apt-get install sshpass\n"
					#command += "sshpass -p \"verma\" ssh red@192.168.31.29 \"exit\"\n"
					command += "sshpass -p \"Akanksha21!\" ssh akanksha@192.168.31.244 \"exit\"\n"
					#command += "echo \"verma\" | sshfs red@192.168.31.29:/Users/red/Documents/nfs_server" + Model_Link +" ~"+ Model_Link +" -o password_stdin"
					command += "echo \"Akanksha21!\" | sshfs akanksha@192.168.31.244:/mnt/Repository" + Model_Link +" ~"+ Model_Link +" -o password_stdin"
					file.write(command)
					file.close()
					time.sleep(5)

					os.system("bash transfer_model.sh " +IP_username_password[IPs[j]][0] + " " + IPs[j] + " " + IP_username_password[IPs[j]][1])
					request_msg_model["Model_Link"].append([IPs[j], "~" + Model_Link])
					j = j + 1

		Services = self.App["Services"]
		for service in Services:
			if service["Criticality"] == "Low":
				Service_Link = service["Service_Link"]
				No_Instances = int(service["No_Instances"])
				print("\nSERVICE BEING INSTALLED: " + Service_Link + " INSTANCES:" + str(No_Instances))
				for i in range(No_Instances):
					file = open("NFS_Mount2.sh", "w")
					command = "mkdir -p ~" + Service_Link + "\n"
					command += "echo " + IP_username_password[IPs[j]][1] + " | sudo -S apt-get install sshpass\n"
					#command += "sshpass -p \"verma\" ssh red@192.168.31.29 \"exit\"\n"
					command += "sshpass -p \"Akanksha21!\" ssh akanksha@192.168.31.244 \"exit\"\n"
					#command += "echo \"verma\" | sshfs red@192.168.31.29:/Users/red/Documents/nfs_server/" + Service_Link +" ~/" + str(self.App["AppDev_ID"]) + "/" + str(self.App["App_ID"]) + "/Services -o password_stdin"
					command += "echo \"Akanksha21!\" | sshfs akanksha@192.168.31.244:/mnt/Repository" + Service_Link +" ~" + Service_Link + " -o password_stdin"
					file.write(command)
					file.close()
					time.sleep(5)

					os.system("bash transfer_service.sh " +IP_username_password[IPs[j]][0] + " " + IPs[j] + " " + IP_username_password[IPs[j]][1])
					request_msg_service["Service_Link"].append([IPs[j], "~" + Service_Link])
					j = j + 1


		App_Link = self.App["App_Link"]
		print("\nAPP BEING INSTALLED:", App_Link)
		file = open("NFS_Mount3.sh", "w")
		command = "mkdir -p ~/" + str(self.App["AppDev_ID"]) + "/" + str(self.App["App_ID"]) + "/AppLogic\n"
		command += "echo " + IP_username_password[IPs[j]][1] + " | sudo -S apt-get install sshpass\n"
		#command += "sshpass -p \"verma\" ssh red@192.168.31.29 \"exit\"\n"
		command += "sshpass -p \"Akanksha21!\" ssh akanksha@192.168.31.244 \"exit\"\n"
		#command += "echo \"verma\" | sshfs red@192.168.31.29:/Users/red/Documents/nfs_server/" + str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"])+"/AppLogic ~"+ App_Link +" -o password_stdin"
		command += "echo \"Akanksha21!\" | sshfs akanksha@192.168.31.244:/mnt/Repository/" + str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"])+"/AppLogic ~"+ App_Link +" -o password_stdin"
		file.write(command)
		file.close()
		time.sleep(5)

		os.system("bash transfer_app.sh " +IP_username_password[IPs[j]][0] + " " + IPs[j] + " " + IP_username_password[IPs[j]][1])
		request_msg_app["App_Link"].append([IPs[j], "~" + App_Link])

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

	def Gateway_Deploy(self):
		IPs = self.App["IPs"]

		request_msg_model = {}
		request_msg_model["Request_Type"] = "Start_Model"
		request_msg_model["Service_ID"] = App["App_ID"]
		request_msg_model["Hosts"] = []

		for ip in IPs:
			file = open("NFS_Mount.sh", "w")
			command = "mkdir -p ~/" + str(self.App["App_ID"]) + "/Models\n"
			command += "echo " + IP_username_password[ip][1] + " | sudo -S apt-get install sshpass\n"
			command += "sshpass -p \"verma\" ssh red@192.168.31.29 \"exit\"\n"
			command += "echo \"verma\" | sshfs red@192.168.31.29:/Users/red/Documents/nfs_server/" + str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"])+"/Models ~/"+str(self.App["App_ID"])+"/Models -o password_stdin"
			file.write(command)
			file.close()
			time.sleep(5)

			os.system("bash transfer_model.sh " +IP_username_password[ip][0] + " " + ip + " " + IP_username_password[ip][1])
			#os.system('echo %s | sudo -S %s' % ("verma", command))
			request_msg_model["Hosts"].append(ip)
		json_request_msg_model = json.dumps(request_msg_model)
		return json_request_msg_model

def callback_LB(ch, method, properties, body):
	print("Receiving IPs from Load Balancer")
	Receiving_Message = json.loads(body)
	# Load Balancer gives unique IPs ALWAYS!!!!
	hm_obj.Host_Deploy(Receiving_Message)

def callback_LBM(ch, method, properties, body):
	print("Receiving IPs from Load Balancer")
	Receiving_Message = json.loads(body)
	# Load Balancer gives unique IPs ALWAYS!!!!
	hm_obj.Model_Deploy(Receiving_Message)

def callback_LBS(ch, method, properties, body):
	print("Receiving IPs from Load Balancer")
	Receiving_Message = json.loads(body)
	# Load Balancer gives unique IPs ALWAYS!!!!
	hm_obj.Service_Deploy(Receiving_Message)

def callback_DM(ch, method, properties, body):
	global port
	print ("Receiving links from Deplyment Manager")

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
		msg_obj.receive(callback_LBS, "", "LB_HM")

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
		msg_obj.receive(callback_LBM, "", "LB_HM")

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
			if model["Criticality"] == "Low":
				Instances += int(model["No_Instances"])
		Services = hm_obj.App["Services"]
		for service in Services:
			if service["Criticality"] == "Low":
				Instances += int(service["No_Instances"])

		req_obj_LB["Type"] = "Host"
		req_obj_LB["Number"] = str(Instances)
		req_obj_LB_json = json.dumps(req_obj_LB)
		msg_obj.send("", "HM_LB", req_obj_LB_json)
		msg_obj.receive(callback_LB, "", "LB_HM")

	if(Request_Type == "Gateway_Deploy"):
		hm_obj.App["Model_Link"] = Receiving_Message["Model_Link"]
		hm_obj.App["AppDev_ID"] = Receiving_Message["AD_ID"]
		hm_obj.App["App_ID"] = Receiving_Message["App_Id"]
		hm_obj.App["IPs"] = Receiving_Message["Gateway_IPs"]

		model = hm_obj.Gateway_Deploy()
		#obj = RabbitMQ()
		msg_obj.send("", "HM_SM", model)
		print("\n\nSent request to SM: ", model)

def listen_DM():

	#Receive Application info from Deployment Manager
	msg_obj.receive(callback_DM, "", "DM_HM")


def listen_FM():

	msg_obj.receive(callback_DM, "", "FM_HM")

def listen_MT():

	msg_obj.receive(callback_DM, "", "MT_HM")

msg_obj = RabbitMQ()
hm_obj = host_manager()

msg_obj.create_queue("", "MT_RM")
msg_obj.create_ServiceQueues("DM","RG")
msg_obj.create_ServiceQueues("HM", "LB")
msg_obj.create_ServiceQueues("SM", "RG")
msg_obj.create_ServiceQueues("DM", "HM")
msg_obj.create_ServiceQueues("FM", "HM")

t1 = threading.Thread(target = listen_DM)
t2 = threading.Thread(target = listen_FM)
t3 = threading.Thread(target = listen_MT)

t1.start()
t2.start()
t3.start()
# #TESTING
# test_obj = json.dumps(test_obj)
# callback_DM(1, 2, 3, test_obj)