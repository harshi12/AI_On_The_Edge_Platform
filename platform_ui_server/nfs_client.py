import os

class NFS(object):
    def __init__(self, serverIP, password):
        self.password = password
        self.serverIP = serverIP

    def mount(self, sourcePath, destinationPath):
        # serverIP1 = "10.2.40.83"
        # serverIP2 = "192.168.2.1"
        serverPath = '/Users/red/Documents/nfs_server' + sourcePath
        command = 'mount ' + self.serverIP + ':' + serverPath + ' ' + destinationPath 
        print(command)
        os.system('mkdir ' + destinationPath)
        print("Destination %s Created\n" %(destinationPath))

        os.system('echo %s | sudo -S %s' % (self.password, command))
        print("Mount Successful\n")


    def unmount(self, sourcePath):
        command = "umount -f -l " + sourcePath
        os.system('echo %s|sudo -S %s' % (self.password, command))
        print("UnMount Successful\n")

    def copy(self, source, destination):
        command = 'cp -R ' + source + ' ' + destination
        os.system(command)
        print("Data Copied Successfully")
        os.system('echo %s | sudo -S chmod -R 777 %s' %(self.password, destination))

    def mkdir(self, destinationPath):
        os.system('mkdir ' + destinationPath)
        print("%s Created\n" %(destinationPath))
        os.system('echo %s | sudo -S chmod -R 777 %s' %(self.password, destinationPath))

    def listdir(self, path = ''):
        res = os.listdir(path)
        return res

    def delete(self, path):
        os.system('echo yes | sudo -S rm -R ' + path)



