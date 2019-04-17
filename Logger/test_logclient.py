from logger_client import LoggerClient
from queue_req_resp import RabbitMQ
import time

def test():
    LC2 = LoggerClient("test_log.log",console=False)
    LC2.start_logger()
    for i in range(1):
        time.sleep(1)
        LC2.log('This is a warning message')
        LC2.log('This is an error message')    

    LC = LoggerClient("./test_log.log",console=False)
    LC.start_logger()

    LC.log('This is a warning message')
    LC.log('This is an error message') 

test()