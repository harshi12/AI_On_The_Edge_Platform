from logger_client import LoggerClient
from queue_req_resp import RabbitMQ
import time

def test():
    RMQ = RabbitMQ("192.168.43.174","harshita","123", int(5672))
    LC = LoggerClient(RMQ,"test_log.log",console=True)
    LC.start_logger()
    for i in range(4):
        time.sleep(1)
        LC.log('This is a warning message')
        LC.log('This is an error message')    
    return 

test()