#!/bin/bash

filepath=$1

echo $filepath
pip3 install apscheduler
# python3 $filepath'scheduler.py' & echo $! > $filepath'schedulerPID.txt' &

nohup python3 $filepath'scheduler.py' 2>&1 & echo $! > $filepath'schedulerPID.txt'
