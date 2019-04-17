import sys
sys.path.insert (0, '../')
sys.path.insert (0, '../../')
import os.path
from RabbitMQ.message_queue import *

class Counter:
    '''
        A simple counter service
        the filepath is generally a file stored in nfs directory.
        A default path is specified.If not present, the file will be created.
    '''
    def __init__(self, RMQ, filepath = "count.txt"):
        self.RMQ = RMQ
        self.filepath = filepath
    
    def nextCount(self):
        newValue = 1
        try:
            if(os.path.isfile(self.filepath)):
                f = open(self.filepath, 'r')
                lines = f.readlines()
                if(len(lines) != 0):
                    oldValue = int(lines[0])
                    newValue = oldValue + 1
                f.close()

            f = open(self.filepath, 'w+')
            f.write(str(newValue))
            f.close()            
            self.RMQ.send('', "temp", str(newValue))
        except:
            print(sys.exc_info()[0],"occured.")

if __name__ == "__main__":
    RMQ = RabbitMQ()
    ctr = Counter(RMQ)
    ctr.nextCount()