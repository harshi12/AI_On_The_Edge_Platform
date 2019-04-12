import os
from queue_req_resp import RabbitMQ
import json
import threading 
import time

test_obj_DM = {
  	"Request_Type" : "App_Submit",
	"AD_ID" : 2,
	"App_Id": 3,
	"Model_Link" : "/2/3/Models",
	"App_Link" : "/2/3/AppLogic",
	"Service_Link" : "/2/3/Services",
	"Config_Link" : "/2/3/Config"
}

test_obj_FM = {
	"Request_Type": "Gateway_Deploy",
	"AD_ID": 2,
	"App_ID": 3,
	"Model_Link": "/2/3/Models",
	"Gateway_IPs": ["192,168.31.38", "192.168.31.11"]
}

IP_username_password = {"192.168.31.194" : ["sukku", "iforgot"], "192.168.31.38" : ["ravi", "Patel@123"], "192.168.31.124" : ["kaushik", "rama1729"], "192.168.31.34" : ["kratika", "Qwerty987**"]}

class host_manager:

	self.App = {}
	
	def Host_Deploy(self, IP_username_password):
		IPs = self.IP_username_password.keys()
		i = 0

		request_msg_model = {}
		request_msg_model["Request_Type"] = "Start_Model"
		request_msg_model["Service_ID"] = App["App_ID"]
		request_msg_model["Hosts"] = []

		request_msg_app = {}
		request_msg_app["Request_Type"] = "Start_App"
		request_msg_app["Service_ID"] = App["App_ID"]
		request_msg_app["Hosts"] = []

		request_msg_service = {}
		request_msg_service["Request_Type"] = "Start_Service"
		request_msg_service["Service_ID"] = App["App_ID"]
		request_msg_service["Hosts"] = []

		for ip in IPs:
				#First two IPs for downloading model
				if i < 2:

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

				#Download application logic at remot
				if i == 2:
					
					file = open("NFS_Mount.sh", "w")
					command = "mkdir -p ~/" + str(self.App["App_ID"]) + "/AppLogic\n"
					command += "echo " + IP_username_password[ip][1] + " | sudo -S apt-get install sshpass\n"
					command += "sshpass -p \"verma\" ssh red@192.168.31.29 \"exit\"\n"
					command += "echo \"verma\" | sshfs red@192.168.31.29:/Users/red/Documents/nfs_server/" + str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"])+"/AppLogic ~/"+str(self.App["App_ID"])+"/AppLogic -o password_stdin"
					file.write(command)
					file.close()
					time.sleep(5)

					os.system("bash transfer_app.sh " +IP_username_password[ip][0] + " " + ip + " " + IP_username_password[ip][1])
					request_msg_app["Hosts"].append(ip)

				#Download services at host
				if i == 3:
					file = open("NFS_Mount.sh", "w")
					command = "mkdir -p ~/" + str(self.App["App_ID"]) + "/Services\n"
					command += "echo " + IP_username_password[ip][1] + " | sudo -S apt-get install sshpass\n"
					command += "sshpass -p \"verma\" ssh red@192.168.31.29 \"exit\"\n"
					command += "echo \"verma\" | sshfs red@192.168.31.29:/Users/red/Documents/nfs_server/" + str(self.App["AppDev_ID"])+"/"+str(self.App["App_ID"])+"/Services ~/"+str(self.App["App_ID"])+"/Services -o password_stdin"
					file.write(command)
					file.close()
					time.sleep(5)

					os.system("bash transfer_service.sh " +IP_username_password[ip][0] + " " + ip + " " + IP_username_password[ip][1])
					request_msg_service["Hosts"].append(ip)

				i = i + 1

		json_request_msg_model = json.dumps(request_msg_model)
		json_request_msg_app = json.dumps(request_msg_app)
		json_request_msg_service = json.dumps(request_msg_service)
		return json_request_msg_model, json_request_msg_app, json_request_msg_service

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

	# def callback_LB(ch, method, properties, body):
	# 	print("Receiving IPs from Load Balancer")
	# 	Receiving_Message = json.loads(body)
	# 	message = Request_Deploy(Receiving_Message)
	# 	obj = RabbitMQ()
	# 	obj.send("", "HM_SM", message)
	# 	print("\n\nSent request to SM: ", message)

def callback_DM(ch, method, properties, body):
	global port
	print ("Receiving links from Deplyment Manager")

	hm_obj = host_manager()
	Receiving_Message = json.loads(body)
	Request_type = Receiving_Message["Request_Type"]

	if(Request_type == "App_Submit"):
		hm_obj.App["Model_Link"] = Receiving_Message["Model_Link"]
		hm_obj.App["App_Link"] = Receiving_Message["App_Link"]
		hm_obj.App["Config_Link"] = Receiving_Message["Config_Link"]
		hm_obj.App["AppDev_ID"] = Receiving_Message["AD_ID"]
		hm_obj.App["App_ID"] = Receiving_Message["App_Id"]
		hm_obj.App["Service_Link"] = Receiving_Message["Service_Link"]

		print("Model link:", hm_obj.App["Model_Link"])
		print("App ID:", hm_obj.App["App_ID"])
		print("Application ID:", hm_obj.App["AppDev_ID"])

		model, app, service = hm_obj.Host_Deploy(IP_username_password)
		obj = RabbitMQ()
		obj.send("", "HM_SM", model)
		print("\n\nSent request to SM: ", model)
		time.sleep(5)
		obj.send("", "HM_SM", app)
		print("\n\nSent request to SM: ", app)
		time.sleep(5)
		obj.send("", "HM_SM", service)
		print("\n\nSent request to SM: ", service)

		## Send request for 4 hosts from Load Balancer
		# IP_request = "Send_IPs"
		# msg_obj.send("", "HM_LB", IP_request)
		# msg_obj.receive(callback_LB, "", "HM_LB")
		
		# Ack_msg = Request_Deploy(Receiving_Message, port)
		# port += 1
		# message = json.dumps(str(Ack_msg))
		# obj = RabbitMQ()
		# obj.send("", "Docker_SM", message)
		# print("\n\nSent ack: ", message)

	if(Request_type == "Gateway_Deploy"):
		hm_obj.App["Model_Link"] = Receiving_Message["Model_Link"]
		hm_obj.App["AppDev_ID"] = Receiving_Message["AD_ID"]
		hm_obj.App["App_ID"] = Receiving_Message["App_Id"]
		hm_obj.App["IPs"] = Receiving_Message["Gateway_IPs"]

		model = hm_obj.Gateway_Deploy()
		obj = RabbitMQ()
		obj.send("", "HM_SM", model)
		print("\n\nSent request to SM: ", model)

def listen_DM():

	msg_obj = RabbitMQ()
	#Receive Application info from Deployment Manager
	msg_obj.receive(callback_DM, "", "DM_HM")


def listen_FM():

	msg_obj = RabbitMQ()
	msg_obj.receive(callback_DM, "", "FM_HM")

t1 = threading.Thread(target = listen_DM)
t2 = threading.Thread(target = listen_FM)

t1.start()
t2.start()

# #TESTING
# test_obj = json.dumps(test_obj)
# callback_DM(1, 2, 3, test_obj)