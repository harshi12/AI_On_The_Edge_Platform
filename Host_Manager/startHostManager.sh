#!/bin/bash

filepath=$1

python3 $filepath'Host_Manager.py' & echo $! > $filepath'HMPID.txt'

