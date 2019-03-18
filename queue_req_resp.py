#shared queue for communication between gateways and service manager and other such scenarios

import pika
import json

class RabbitMQ:
	def __init__(self):
		self.server_IP = "192.168.43.173"
		self.server_Port = 5672
		self.credentials = pika.PlainCredentials("rajat","123")	
		self.create_queue("", "AD_SM")
		self.create_ServiceQueues("SM","Docker")
		self.create_ServiceQueues("SM", "Scheduler")
		self.create_queue("", "Model1_Input")
		self.create_queue("", "Model1_Output")

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
		# body = channel.basic_get(queue_name, True) #callback, queue = queue_name, no_ack = True)
		print("In queue:", type(body))
		return body

	def receive(self, callback, exchange_name, queue_name):
		channel, conn = self.create_connection()	
		self.create_queue(exchange_name, queue_name)
		channel.basic_consume(callback, queue = queue_name, no_ack = True)

		print(' [*] Waiting for messages. To exit press CTRL+C')
		channel.start_consuming()