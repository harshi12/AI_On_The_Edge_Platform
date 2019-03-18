#Rajat's IP: 192.168.43.173

from queue_req_resp import RabbitMQ

# initial_obj = RabbitMQ(1)

obj = RabbitMQ()#rabbit@Rajat-MacBook_Pro")

def callback(ch, method, properties, body):
	print("data received: %r"%body)

obj.receive(callback, "", "AD_Input")
