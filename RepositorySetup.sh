#!/bin/bash

password=$3
IP=$1
username=$2
network=$4

sshpass -p $password ssh -o StrictHostKeyChecking=no -t $username@$IP << EOF 
  
  echo $password | sudo -S apt-get update
  echo $password | sudo -S apt-get install nfs-kernel-server
  echo $password | sudo -s chmod 777 /etc/exports
  echo $password | sudo -S mkdir /mnt/Repository 
  echo $password | sudo -S chown nobody:nogroup /mnt/Repository
  echo $password | sudo -S chmod 777 /mnt/Repository
  echo $password | sudo -S echo /mnt/Repository $network/24\(rw,sync,no_subtree_check\) > /etc/exports
  echo $password | sudo -S exportfs -a
  echo $password | sudo -S systemctl restart nfs-kernel-server
  echo $password | sudo -S ufw allow from $network/24 to any port nfs
EOF

#service nfs-kernel-server stop -- to stop NFS server

#echo $password | sudo -S apt-get update