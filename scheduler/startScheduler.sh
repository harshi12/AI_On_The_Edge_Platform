#!/bin/bash

filepath=$1

pip3 install apscheduler
python3 $filepath'scheduler.py' & echo $! > $filepath'schedulerPID.txt'

