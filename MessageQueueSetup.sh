#!/bin/bash

password=$2
username=$1

echo "deb http://www.rabbitmq.com/debian/ testing main" >> sudo /etc/apt/sources.list
curl http://www.rabbitmq.com/rabbitmq-signing-key-public.asc | sudo  apt-key add -
echo $password | sudo -S apt-get -q update
echo $password | sudo -S apt-get -q install rabbitmq-server
echo $password | sudo -s chmod 777 /etc/default/rabbitmq-server
echo $password | sudo -S echo ulimit -n 1024  > /etc/default/rabbitmq-server
echo $password | sudo -S service rabbitmq-server start & echo $! > /home/$username/Platform/RMQPID.txt
echo "RabbitMQ PID: $(cat /home/$username/RMQPID.txt)"
echo $password | sudo -S rabbitmq-plugins enable rabbitmq_management
echo $password | sudo -S rabbitmqctl add_user harshita 123
echo $password | sudo -S rabbitmqctl set_user_tags harshita administrator
echo $password | sudo -S rabbitmqctl set_permissions -p / harshita ".*" ".*" ".*"

# To start the service:
#service rabbitmq-server start

# To stop the service:
#service rabbitmq-server stop

# To restart the service:
#service rabbitmq-server restart

# To check the status:
#service rabbitmq-server status
