import xml.etree.ElementTree as ET
import os
# read XML file to look for all the IP:Port and which module will run where

'''
*****Platform Bootstrap******
1. Start NFS Server
2. Start RabbitMQ Server

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
		self.NFSServerIP = 0
		self.RabbitMQIP = 0
		self.RMQCredentials = {}

		
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
		return IP, Port, username, password, setupFileName, setupFilePath

	def mountNFS(self, moduleName):
		IP, Port, username, password, _ = self.getVariables(moduleName)
		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'echo "+password+" | sudo -S apt-get install nfs-common\'"
		print(cmd)
		os.system(cmd)

		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'mkdir -p /home/"+username+"/Platform\'"
		print(cmd)
		os.system(cmd)

		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'echo "+password+" | sudo -S mount "+self.NFSServerIP+":/mnt/Repository /home/"+username+"/Platform/\'"
		print(cmd)
		os.system(cmd)

		return


	def initDeploymentManager():
		pass

	def initServiceManager(self):
		IP, Port, username, password, setupFileName, setupFilePath = self.getVariables('ServiceManager')
		self.mountNFS('ServiceManager')


	def initHostManager():
		pass

	def initLoadBalancer():
		pass

	def initScheduler():
		pass

	def initLogger():
		pass

	def initMonitor():
		pass

	def initRecoveryManager():
		pass

	def initDatabase():
		pass

	def initPlatformUI():
		pass

	def initRegistry():
		pass

	def initNFS(self): 
		IP, Port, username, password, setupFileName, setupFilePath = self.getVariables('Repository')
		temp = IP.split('.')
		network = temp[0]+'.'+temp[1]+'.'+temp[2]+'.'+'0'

		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'mkdir -p /home/"+username+"/Platform\'"
		print(cmd)
		os.system(cmd)

		cmd = "sshpass -p "+password+" scp "+setupFilePath+" "+username+"@"+IP+":/home/"+username+"/Platform/"
		print(cmd)
		os.system(cmd)

		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'/home/"+username+"/"+"/Platform/"+setupFileName+" "+IP+" "+username+" "+password+" "+network+"\'"
		print(cmd)
		os.system(cmd)
		print("Repository setup finished on",IP,"!")
		self.NFSServerIP = IP

	def initRabbitMQServer(self):
		IP, Port, username, password, setupFileName, setupFilePath = self.getVariables('Repository')
		
		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'mkdir -p /home/"+username+"/Platform\'"
		print(cmd)
		os.system(cmd)

		cmd = "sshpass -p "+password+" scp "+setupFilePath+" "+username+"@"+IP+":/home/"+username+"/Platform/"
		print(cmd)
		os.system(cmd)

		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'/home/"+username+"/"+"/Platform/"+setupFileName+" "+IP+" "+username+" "+password+"\'"
		print(cmd)
		os.system(cmd)

		print("RabbitMQ Server started on IP: ",IP)
		self.RabbitMQIP = IP
		self.RMQCredentials['username'] = 'harshita'
		self.RMQCredentials['password'] = '123'


if __name__ == '__main__':
	boot = Bootstrap('platformConfig.xml')
	boot.parsePlatformConfig()
	print("Module Data:",boot.moduleData)
	print("Module Host Credentials:", boot.platformHostCredentials)
	
	boot.initNFS()
	boot.initRabbitMQServer()
	