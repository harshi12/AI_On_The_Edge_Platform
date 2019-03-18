#shared queue for communication between gateways and service manager and other such scenarios

import pika
import json

class RabbitMQ:
	def __init__(self,server_IP):
		self.server_IP = str(server_IP)

	def send(self,message):
		connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost')) #self.server_IP))
		channel = connection.channel()

		channel.queue_declare(queue='queue_gateway_ServiceManager')
		# message = ' '.join(sys.argv[1:]) or "Hello World!"
		channel.basic_publish(exchange='',
		                      routing_key='queue_gateway_ServiceManager',
		                      body=message)
		print(" [x] Sent",message)
		connection.close()

	def receive(self):
		connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))#self.server_IP))
		channel = connection.channel()

		channel.queue_declare(queue = 'queue_gateway_ServiceManager')

		def callback(ch, method, properties, body):
		    print(" [x] Received %r" % body)

		channel.basic_consume(callback,
		                      queue = 'queue_gateway_ServiceManager',
		                      no_ack = True)

		print(' [*] Waiting for messages. To exit press CTRL+C')
		channel.start_consuming()