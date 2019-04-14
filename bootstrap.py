import xml.etree.ElementTree as ET
import os
# read XML file to look for all the IP:Port and which module will run where

'''
*****Platform Bootstrap******
1. Start NFS Server
2. Start RabbitMQ Server
3. Start Service Manager


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
		self.RabbitMQIP = 0	
		self.RabbitMQPort = 5672
		self.RMQCredentials = {}
		self.NFSpid = 0
		self.RMQInput = ""

		
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
		path = '/home/'+username+'/Platform/'
		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'mkdir -p "+path+"\'"
		print(cmd)
		os.system(cmd)
		return path

	def getFolderPath(self, mountPath, setupFilePath):
		setupFilePath = mountPath +'/'+setupFilePath 
		temp = setupFilePath.split('/')
		print("temp", temp)
		folderPath = ""
		for i in temp[:-1]:
			folderPath += i+'/'

		return folderPath

	def mountNFS(self, moduleName):
		IP, Port, username, password, temp1, temp2 = self.getVariables(moduleName)
		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'echo "+password+" | sudo -S apt-get install nfs-common\'"
		print(cmd)
		os.system(cmd)

		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'mkdir -p /home/"+username+"/Platform\'"
		print(cmd)
		os.system(cmd)

		mountPath = '/home/'+username+'/Platform'
		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'echo "+password+" | sudo -S mount "+self.NFSServerIP+":/mnt/Repository "+mountPath+"\'"
		print(cmd)
		os.system(cmd)

		return mountPath


	def initDeploymentManager():
		pass

	def initServiceManager(self):
		IP, Port, username, password, setupFileName, setupFilePath = self.getVariables('ServiceManager')
		path = self.mountNFS('ServiceManager')
		
		# setupFilePath = path +'/'+setupFilePath 
		# temp = setupFilePath.split('/')
		# print("temp", temp)
		folderPath = getFolderPath(path, setupFilePath)
		# for i in temp[:-1]:
		# 	folderPath += i+'/'

		print("folderPath", folderPath)
		# RMQInput = self.RabbitMQIP+" "+self.RabbitMQPort+" "+self.RMQCredentials['username']+" "+self.RMQCredentials['password']
		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'"+setupFilePath+" "+folderPath+" "+self.RMQInput+"\'"
		print(cmd)
		os.system(cmd)		
		print('Service Manager started on IP', IP)


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
		IP, Port, username, password, setupFileName, setupFilePath = self.getVariables('Registry')
		path = createPath(self, username, password, IP)
		path = self.mountNFS('Registry')
		folderPath = getFolderPath(path, setupFilePath)
		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'"+setupFilePath+" "+folderPath+" "+self.RMQInput+"\'"
		print(cmd)
		os.system(cmd)		
		print('Registry started on IP', IP)
		

	def initNFS(self): 
		IP, Port, username, password, setupFileName, setupFilePath = self.getVariables('Repository')
		print("**************************", IP)
		temp = IP.split('.')
		network = temp[0]+'.'+temp[1]+'.'+temp[2]+'.'+'0'
		print("**************************", network)

		path = createPath(self, username, password, IP)
		# path = '/home/'+username+'/Platform/'
		# cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'mkdir -p "+path+"\'"
		# print(cmd)
		# os.system(cmd)

		cmd = "sshpass -p "+password+" scp "+setupFilePath+" "+username+"@"+IP+":"+path
		print(cmd)
		os.system(cmd)

		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'/home/"+username+"/Platform/"+setupFileName+" "+IP+" "+username+" "+password+" "+network+"\'"
		print(cmd)
		os.system(cmd)

		path = username+'@'+IP+':'+path+'repoPID.txt'
		cmd = "sshpass -p "+password+" scp "+path+"  ./"
		print(cmd)
		os.system(cmd)

		with open('repoPID.txt') as f:
			pid = f.read()
			self.NFSpid = pid

		print("Repository setup finished on",IP,"!")
		self.NFSServerIP = IP

	def initRabbitMQServer(self):
		IP, Port, username, password, setupFileName, setupFilePath = self.getVariables('RabbitMQServer')
		
		path = createPath(self, username, password, IP)
		# cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'mkdir -p /home/"+username+"/Platform\'"
		# print(cmd)
		# os.system(cmd)

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
		self.RMQInput = IP+" "+Port+" "+harshita+" 123"


if __name__ == '__main__':
	boot = Bootstrap('platformConfig.xml')
	boot.parsePlatformConfig()

	boot.initNFS()
	boot.initRegistry()
	# boot.initRabbitMQServer()
	# boot.initServiceManager()
