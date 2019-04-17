#!/bin/bash

filepath=$1

python3 $filepath'monitor.py' & echo $! > $filepath'monitorPID.txt'

