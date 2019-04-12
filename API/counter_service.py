import sys
import os.path

class Counter:
    '''
        A simple counter service
        the filepath is generally a file stored in nfs directory.
        A default path is specified.If not present, the file will be created.
    '''
    def __init__(self, filepath = "count.txt"):
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
            # write code here to send this newValue to the output stream

        except:
            print(sys.exc_info()[0],"occured.")