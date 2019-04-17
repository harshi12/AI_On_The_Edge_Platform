#!/bin/bash

filepath=$1

# python3 $filepath'monitor.py' & echo $! > $filepath'monitorPID.txt'

nohup python3 $filepath'monitor.py' 2>&1 & echo $! > $filepath'monitorPID.txt'
