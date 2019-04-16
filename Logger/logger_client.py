from queue_req_resp import RabbitMQ
import queue
import logging
from logging.handlers import QueueHandler, QueueListener
import datetime

class LoggerClient():
    def __init__(self,RMQ,logfile_path,console=False):
        """
        Logger API at Client Side to store the logs locally and sent to Central Logger MQ
        Parameters - RMQ - Create a RabbitMQ Object and pass it 
                   - logfile_path - Path where to create log file
                   - console - whether to diaplay log messages on screen - Default false
        """
        self.RMQ = RMQ
         #Creating queue and logger
        self.log_queue = queue.Queue(-1)   #infinite size
        self.queue_handler = QueueHandler(self.log_queue)
        self.logger = logging.getLogger()
        self.logger.addHandler(self.queue_handler)
        #formatter
        self.formatter = logging.Formatter(' %(message)s')
        #file handler - write to file
        self.file_handler_loc = logging.FileHandler(logfile_path)
        self.file_handler_loc.setFormatter(self.formatter)
        #console handler - print on screen
        if(console == True):
            self.console_handler = logging.StreamHandler()
            self.console_handler.setFormatter(self.formatter)
            self.listener = QueueListener(self.log_queue,self.console_handler,self.file_handler_loc )
        else:
            self.listener = QueueListener(self.log_queue,self.file_handler_loc )


    def start_logger(self):
        self.listener.start()

    def emit(self, record):
        return self.queue_handler.emit(record)

    def __del__(self):
        self.listener.stop()

    def log(self,msg):
        time=datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")
        msg="["+time+"] : "+msg
        self.logger.error(msg)
        msg+="\n"
        self.RMQ.send("", "To_Log", msg)

###README
#Create RabbitMQ Object
#Create LoogerClient Object by passing required parameters
#call start_logger() using this Object
#Now you can use this object to log - call Object.log(msg)
#The log message will be saved along with date in local log file (file_path in parameters) and send to central logger through queue (and also to the console based on parameter passed)
#Example: (test_logclient.py)
#----------------------------
# from logger_client import LoggerClient
# from queue_req_resp import RabbitMQ
# import time

# def test():
#     RMQ = RabbitMQ("192.168.43.174","harshita","123", int(5672))
#     LC = LoggerClient(RMQ,"test_log.log",console=True)
#     LC.start_logger()
#     for i in range(4):
#         time.sleep(1)
#         LC.log('This is a warning message')
#         LC.log('This is an error message')    
#     return 

# test()
