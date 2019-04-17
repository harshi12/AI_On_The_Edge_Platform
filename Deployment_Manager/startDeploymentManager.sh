#!/bin/bash

filepath=$1

# python3 $filepath'Deployment_Manager.py' & echo $! > $filepath'DMPID.txt'

nohup python3 $filepath'Deployment_Manager.py' 2>&1 & echo $! > $filepath'DMPID.txt'