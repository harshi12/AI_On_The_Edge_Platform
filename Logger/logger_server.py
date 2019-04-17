import queue
import logging
from logging.handlers import QueueHandler, QueueListener
from queue_req_resp import RabbitMQ
from threading import Thread


FILE_PATH_SERVER = "/home/sukku/Downloads/IAS/logs/server_log.log"

class LoggerServer():
    def __init__(self,RMQ):
        """
        Logger API at Server Side (Central Logger) to store the logs from all the modules
        """
        #RabbitMQQueue
        self.RMQ = RMQ
        # self.RMQ.create_queue("","To_Log")
        t1 = Thread(target = self.receiveInputLog, args = ('', "To_Log")) #thread that will monitor To_Log Queue
        t1.start()
    
    # Function that will monitor To_Log Queue - to receive startService from DM
    def receiveInputLog(self, exchange, key):
        print(exchange)
        print(key)
        print("Listening......")
        self.RMQ.receive(self.processInputLog, exchange, key)

    def processInputLog(self, ch, method, properties, body):
        # data = json.loads(body)
        print(body)
        f = open(FILE_PATH_SERVER, "a")
        f.write(body)
        f.close()


if __name__ == "__main__":
    RMQ = RabbitMQ()    
    LS = LoggerServer(RMQ)
