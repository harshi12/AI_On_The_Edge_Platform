#!/bin/bash

filepath=$1

python3 $filepath'registry.py' & echo $! > $filepath'regsitryPID.txt'
