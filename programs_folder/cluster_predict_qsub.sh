#!/bin/bash
#Launching script for Test
#Submission options
#$-S /bin/bash

execution_folder=/home/alexandre/Desktop/workspace/Projet_M2/programs_folder
cd "$execution_folder"
python2.7 cluster_predict.py $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10}
