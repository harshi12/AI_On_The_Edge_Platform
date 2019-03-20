import os
from queue_req_resp import RabbitMQ
import json

port = 8500
model_ip_port = {}
IP_username_password = {"192.168.43.103" : ["sukku", "iforgot"], "192.168.43.137" : ["ravi", "S2j1ar1in63"], "192.168.43.76" : ["bhavidhingra", "bhavi"]}

def Request_Deploy(Receiving_Message, Port):
	global port
	IPs = Receiving_Message["IPs"]
	model_link = Receiving_Message["Link"]
	Docker_Name = model_link

	Ack_msg = {}
	Ack_msg["Ack"] = {"Model": model_link , "IP:Port": []}

	for ip in IPs:

		if model_link not in model_ip_port.keys() or ip not in model_ip_port[model_link]:

			if model_link not in model_ip_port.keys():
				model_ip_port[model_link] = []

			#Install Docker on remote machine
			print("Installing docker at remote\n")
			print("sshpass -p \'" + IP_username_password[ip][1] + "\' ssh -t " + IP_username_password[ip][0] + "@" + ip + " \'bash \' < install_docker.sh \'" + IP_username_password[ip][1] + 
				"\'")
			os.system("sshpass -p \'" + IP_username_password[ip][1] + "\' ssh -t " + IP_username_password[ip][0] + "@" + ip + " \'bash \' < install_docker.sh \'" + IP_username_password[ip][1] + 
				"\'")

			#Download model from Github link
			print("Downloading Github link at remote\n")
			print("sshpass -p \'" + IP_username_password[ip][1] + "\' ssh " + IP_username_password[ip][0] + "@" + ip + " python3 < Pkg_Downloader.py - \"" + model_link + 
				"\" \"" + IP_username_password[ip][0] + "\"")
			os.system("sshpass -p \'" + IP_username_password[ip][1] + "\' ssh " + IP_username_password[ip][0] + "@" + ip + " python3 < Pkg_Downloader.py - \"" + model_link + 
				"\" \"" + IP_username_password[ip][0] + "\"")

			#Create directory named as model link
			print("sshpass -p \'" + IP_username_password[ip][1] + "\' ssh " + IP_username_password[ip][0] + "@" + ip + " mkdir " + model_link)
			os.system("sshpass -p \'" + IP_username_password[ip][1] + "\' ssh " + IP_username_password[ip][0] + "@" + ip + " mkdir " + model_link)

			#Extract Model zip file
			print("Extracting model at remote\n")
			print("sshpass -p \'" + IP_username_password[ip][1] + "\' ssh " + IP_username_password[ip][0] + "@" + ip + " unzip " + model_link + ".zip -d ./" + model_link)
			os.system("sshpass -p \'" + IP_username_password[ip][1] + "\' ssh " + IP_username_password[ip][0] + "@" + ip + " unzip " + model_link + ".zip -d ./" + model_link)

			model_ip_port[Docker_Name].append(ip)

		#model_ip_port[model_link].append(ip)
		Command = "docker run -t --name " + Docker_Name + " --rm -p " + str(port) + ":8501 -v /home/" + IP_username_password[ip][0] + "/" + model_link + "/model:/models/" + model_link +" -e MODEL_NAME="+ model_link +" tensorflow/serving &"
		#print (Command)
		os.system("sshpass -p \'" + IP_username_password[ip][1] + "\' ssh " + IP_username_password[ip][0] + "@" + ip + " " +Command)
		Ack_msg["Ack"]["IP:Port"].append(ip + ":" + str(port))
	return Ack_msg

def Request_Kill(Receiving_Message):
    Docker_Id = Receiving_Message["Link"]
    for ip in model_ip_port[Docker_Id]:
    	print("In Kill. Kill at IP:", ip)
    	Command = "docker kill "+ Docker_Id
    	os.system("sshpass -p \'" + IP_username_password[ip][1] + "\' ssh " + IP_username_password[ip][0] + "@" + ip + " " +Command)
    #Dummy_Docker_Id = os.popen("docker kill "+Docker_Id).read()[:-1]

def callback(ch, method, properties, body):
	global port
	print ("Receiving")
	body = body.decode("utf-8").replace('\0', '')
	#Receiving_Message = json.loads(body).replace('\'','\"')
	Receiving_Message = json.loads(body)
	Request_type = Receiving_Message["Request_type"]
	if(Request_type == "Deploy"):
		Ack_msg = Request_Deploy(Receiving_Message, port)
		port += 1
		message = json.dumps(str(Ack_msg))
		obj = RabbitMQ()
		obj.send("", "Docker_SM", message)
		print("\n\nSent ack: ", message)

	if(Request_type == "Kill"):
		Request_Kill(Receiving_Message)



# while(1):

#RabbitMQ object
msg_obj = RabbitMQ()
msg_obj.receive(callback, "", "SM_Docker")
	