#!/bin/bash

password=$2
username=$1
network=$3
  
  echo $password | sudo -S apt-get -q update
  echo $password | sudo -S apt-get -q install nfs-kernel-server
  echo $password | sudo -s chmod 777 /etc/exports
  echo $password | sudo -S mkdir /mnt/Repository 
  echo $password | sudo -S chown nobody:nogroup /mnt/Repository
  echo $password | sudo -S chmod 777 /mnt/Repository
  echo $password | sudo -S echo /mnt/Repository $network/24\(rw,sync,no_subtree_check\) > /etc/exports
  echo $password | sudo -S exportfs -a
  # nohup python3 $filepath'hack3ServiceManager.py' 2>&1 & echo $! > $filepath'SMPID.txt'

  nohup echo $password | sudo -S service nfs-kernel-server start 2>&1 & echo $! > /mnt/Repository/repoPID.txt
  echo $password | sudo -S ufw allow from $network/24 to any port nfs

#service nfs-kernel-server stop -- to stop NFS server

#echo $password | sudo -S apt-get update