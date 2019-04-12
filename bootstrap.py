import xml.etree.ElementTree as ET
import os
# read XML file to look for all the IP:Port and which module will run where

'''
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


	def initDeploymentManager():
		pass

	def initServiceManager(self):
		IP = self.moduleIPPort['ServiceManager']['IP']
		Port = self.moduleIPPort['ServiceManager']['Port']


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
		# set NFS server IP
		# start NFS server using command line
		# install NFS common module
		IP = self.moduleData['Repository']['IP']
		Port = self.moduleData['Repository']['Port']
		username = self.platformHostCredentials[IP]['username']
		password = self.platformHostCredentials[IP]['password']
		setupFileName = self.moduleData['Repository']['executableFile'].strip()
		setupFilePath = (self.moduleData['Repository']['folderName'] + '/' + setupFileName).strip()
		temp = IP.split('.')
		network = temp[0]+'.'+temp[1]+'.'+temp[2]+'.'+'0'

		cmd = cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'mkdir -p /home/"+username+"/Platform\'"
		print(cmd)
		os.system(cmd)

		cmd = "sshpass -p "+password+" scp "+setupFilePath+" "+username+"@"+IP+":/home/"+username+"/Platform/"
		print(cmd)
		os.system(cmd)

		cmd = "sshpass -p "+password+" ssh -o StrictHostKeyChecking=no -t "+username+"@"+IP+" \'/home/"+username+"/"+"/Platform/"+setupFileName+" "+IP+" "+username+" "+password+" "+network+"\'"
		print(cmd)
		os.system(cmd)
		print("Repository setup finished on",IP,"!")

	def initRabbitMQServer(self):
		pass


if __name__ == '__main__':
	boot = Bootstrap('platformConfig.xml')
	boot.parsePlatformConfig()
	print("Module Data:",boot.moduleData)
	print("Module Host Credentials:", boot.platformHostCredentials)
	boot.initNFS()