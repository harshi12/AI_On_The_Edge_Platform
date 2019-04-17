#!/bin/bash

filepath=$1

# python3 $filepath'Host_Manager.py' & echo $! > $filepath'HMPID.txt'

nohup python3 $filepath'Host_Manager.py' 2>&1 & echo $! > $filepath'HMPID.txt'

