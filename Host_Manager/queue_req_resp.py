#shared queue for communication between gateways and service manager and other such scenarios

import pika
import json

RMQFile = "RMQCredentials.txt"

class RabbitMQ:
	def __init__(self):
		with open('RMQCredentials.txt', 'r') as f:
			data = json.load(f)

		self.server_IP = data["IP"]
		self.server_Port = data["Port"]
		self.credentials = pika.PlainCredentials(data["username"], data["password"])	
		self.create_queue("", "AD_SM")
		self.create_ServiceQueues("SM","Docker")
		self.create_ServiceQueues("SM", "Scheduler")

	def create_queue(self, exchange_name, queue_name):
		channel, conn = self.create_connection()
		# channel.exchange_declare(exchange='', exchange_type='direct')
		channel.queue_declare(queue = queue_name, durable = True)
		# channel.queue_bind(exchange=exchange_name, queue=queue_name)
		conn.close()

	def create_ServiceQueues(self,Module1, Module2):
		self.create_queue("", str(Module1+"_"+Module2))
		self.create_queue("", str(Module2+"_"+Module1))

	def create_connection(self):
		connection = pika.BlockingConnection(pika.ConnectionParameters(self.server_IP, self.server_Port, '/', self.credentials))
		channel = connection.channel()
		return channel, connection

	def send(self,exchange_name, queue_name, message):
		channel, conn = self.create_connection()
		self.create_queue(exchange_name, queue_name)
		channel.basic_publish(exchange='', routing_key=queue_name, body=message)
		print(" [x] Sent",message)
		conn.close()

	def receive_nonblock(self, exchange_name, queue_name):
		channel, conn = self.create_connection()	
		self.create_queue(exchange_name, queue_name)
		method_frame, header_frame, body = channel.basic_get(queue_name, True)

		if body == None:
			while body == None:
				method_frame, header_frame, body = channel.basic_get(queue_name, True)

		# body = channel.basic_get(queue_name, True) #callback, queue = queue_name, no_ack = True)
		print("In queue:", type(body))
		return body

	def receive(self, callback, exchange_name, queue_name):
		channel, conn = self.create_connection()	
		self.create_queue(exchange_name, queue_name)

		channel.basic_consume(on_message_callback = callback, queue = queue_name, auto_ack = True)

		print(' [*] Waiting for messages. To exit press CTRL+C')
		channel.start_consuming()