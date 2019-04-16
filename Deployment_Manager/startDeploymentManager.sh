#!/bin/bash

filepath=$1

python3 $filepath'Deployment_Manager.py' & echo $! > $filepath'DMPID.txt'

