#Rajat's IP: 192.168.43.173

from queue_req_resp import RabbitMQ

# initial_obj = RabbitMQ(1)

obj = RabbitMQ()
obj.send("", "AD_Input", "Hello from the other side")