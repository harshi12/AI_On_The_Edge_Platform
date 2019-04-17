#!/bin/bash

filepath=$1

# python3 $filepath'registry.py' & echo $! > $filepath'regsitryPID.txt'
echo $PWD
nohup python3 $filepath'registry.py' 2>&1 & echo $! > $filepath'regsitryPID.txt'
