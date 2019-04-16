#!/bin/bash

filepath=$1

python3 $filepath'hack3ServiceManager.py' & echo $! > $filepath'SMPID.txt'
