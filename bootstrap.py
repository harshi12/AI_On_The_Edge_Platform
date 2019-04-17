import xml.etree.ElementTree as ET
import os
import json
# read XML file to look for all the IP:Port and which module will run where

'''
*****Platform Bootstrap******
1. Start NFS Server
2. Start Registry
3. Start RabbitMQ Server
4. Start Service Manager


STEPS:
1. mount NFS API folder on all the host machines
2. install the dependency if any for each module
'''

class Bootstrap:
	def __init__(self, PlatformConfig): 
		# PlatformConfig is the path to the platform configuration file
		tree = ET.parse(PlatformConfig)		
		self.root = tree.getroot()

		#create a dictionary to store IP, port where each module will run
		self.moduleData = {}
		# create a dictionary to store username password of each host machine in the platform
		self.platformHostCredentials = {}
		self.NFSServerIP = "10.3.10.86"
		self.RabbitMQIP = "10.3.10.86"
		self.RabbitMQPort = 5672
		self.RMQCredentials = {}
		self.NFSpid = 0
		self.RMQInput = ""
		self.NFSMounted = []
		self.ModulesInfo = []

		
	def parsePlatformConfig(self):
		for children in self.root.iter('platformModules'):
			for child in children:
				attribDictionary = child.attrib
				moduleName = attribDictionary['name']
				self.moduleData[moduleName] = {}

				for elements in child:
					self.moduleData[moduleName][elements.tag] = elements.text

		for children in self.root.iter('Hosts'):
			for child in children:
				attribDictionary = child.attrib
				hostIP = attribDictionary['IP']
				self.platformHostCredentials[hostIP] = {}

				for elements in child:
					self.platformHostCredentials[hostIP][elements.tag] = elements.text

	def getVariables(self, moduleName):
		IP = self.moduleData[moduleName]['IP']
		Port = self.moduleData[moduleName]['Port']
		username = self.platformHostCredentials[IP]['username']
		password = self.platformHostCredentials[IP]['password']
		setupFileName = self.moduleData[moduleName]['executableFile'].strip()
		setupFilePath = (self.moduleData[moduleName]['folderName'] + '/' + setupFileName).strip()
		setupFilePath = setupFilePath.replace(" ", "\ ")
		return IP, Port, username, password, setupFileName, setupFilePath

	def createPath(self, username, password, IP):
		# will create path like /home/harshita/Platform on the given IP
		path = '/home/'+username+'/Platform/'
		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'mkdir -p "+path+"\'"
		print(cmd)
		os.system(cmd)
		return path

	def getFolderPath(self, mountPath, setupFilePath):
		# return folderPath like /home/harshita/Platform/Service_Manager/
		# mountPath = /home/harshita/Platform/
		#setupFilePath = ./setupFile.sh or ./ServiceManager/startupFile.sh
		setupFilePath = mountPath + setupFilePath 

		temp = setupFilePath.rfind('/')
		folderPath = setupFilePath[:temp]

		return folderPath+'/'

	def mountNFS(self, moduleName):
		# mount the repository on the host machine /home/harshita/Platform
		IP, Port, username, password, setupFileName, setupFilePath = self.getVariables(moduleName)
		if IP in self.NFSMounted:
			return '/home/'+username+'/Platform/'
		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'echo "+password+" | sudo -S apt-get install nfs-common\'"
		print(cmd)
		os.system(cmd)

		mountFolder = setupFilePath.split('/')[0]
		mountPath = '/home/'+username+'/Platform/'
		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'echo "+password+" | sudo -S mount "+self.NFSServerIP+":/mnt/Repository/"+" "+mountPath+"\'"
		print(cmd)
		os.system(cmd)

		self.NFSMounted.append(IP)

		return mountPath


	def storeModuleInfo(self, IP, port, username, password, filepath, moduleName):
		cmd = "sshpass -p "+password+" scp "+filepath+"  ./"
		print(cmd)
		os.system(cmd)

		temp = {}
		temp["ModuleName"] = moduleName
		temp["IP"] = IP

		ind = filepath.rfind('/')
		filename = filepath[ind+1:]
		with open(filename) as f:
			pid = f.read()
			temp["PID"] = pid

		self.ModulesInfo.append(temp)
		print(moduleName,"setup finished on",IP,"pid is:", pid)

	def startModule(self, moduleName, pidFileName):
		IP, Port, username, password, setupFileName, setupFilePath = self.getVariables(moduleName)
		path = self.createPath(username, password, IP)
		path = self.mountNFS(moduleName)
		folderPath = self.getFolderPath(path, setupFilePath)
		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'"+folderPath+setupFileName+" "+folderPath+"\'"
		print(cmd)
		os.system(cmd)		

		self.storeModuleInfo(IP, Port, username, password, folderPath+pidFileName, moduleName)
		print(moduleName,'started on IP', IP)

	def initDeploymentManager(self):
		self.startModule('DeploymentManager', "DMPID.txt")

	def initServiceManager(self):
		self.startModule('ServiceManager', "SMPID.txt")
		
	def initHostManager(self):
		self.startModule("HostManager", "HMPID.txt")

	def initLoadBalancer():
		pass

	def initScheduler(self):
		self.startModule("Scheduler", "schedulerPID.txt")

	def initLogger():
		pass

	def initMonitor(self):
		self.startModule("Monitor", "monitorPID.txt")
		

	def initRecoveryManager():
		pass

	def initDatabase():
		pass

	def initPlatformUI():
		pass

	def initRegistry(self):
		self.startModule("Registry", "regsitryPID.txt")

	def initNFS(self): 
		IP, Port, username, password, setupFileName, setupFilePath = self.getVariables('Repository')

		temp = IP.split('.')
		network = temp[0]+'.'+temp[1]+'.'+temp[2]+'.'+'0'

		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'/mnt/Repository/"+setupFileName+" "+username+" "+password+" "+network+"\'"
		print(cmd)
		os.system(cmd)

		self.storeModuleInfo(IP, Port, username, password, "/mnt/Repository/repoPID.txt", "Repository")

		self.NFSServerIP = IP

	def initRabbitMQServer(self):
		IP, Port, username, password, setupFileName, setupFilePath = self.getVariables('RabbitMQServer')
		
		path = self.createPath(username, password, IP)
		path = self.mountNFS("RabbitMQServer")

		cmd = "sshpass -p "+password+" scp "+setupFilePath+" "+username+"@"+IP+":"+path
		print(cmd)
		os.system(cmd)

		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'/home/"+username+"/Platform/"+setupFileName+" "+username+" "+password+"\'"
		print(cmd)
		os.system(cmd)

		print("RabbitMQ Server started on IP: ",IP)
		RMQdic = {"IP" : IP, "Port" : Port, "username" : "harshita", "password" : "123"}
		

		filename = '/home/'+username+'/Platform/RMQCredentials.txt'
		with open(filename, 'w') as f:
			json.dump(RMQdic, f)

		path = self.getFolderPath(path, setupFilePath)
		self.storeModuleInfo(IP, Port, username, password, path+"RMQPID.txt", "RabbitMQServer")

		self.RabbitMQIP = IP
		self.RMQCredentials['username'] = 'harshita'
		self.RMQCredentials['password'] = '123'
		self.RMQInput = IP+" "+Port+" "+"harshita"+" 123"


if __name__ == '__main__':
	boot = Bootstrap('platformConfig.xml')
	boot.parsePlatformConfig()

	# boot.initNFS()
	boot.initRegistry()
	# boot.initRabbitMQServer()
	boot.initServiceManager()
	boot.initDeploymentManager()
	boot.initHostManager()
	boot.initMonitor()
	boot.initScheduler()
	print(boot.ModulesInfo)