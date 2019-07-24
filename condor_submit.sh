#!/bin/bash

# For HTCondor FarmSubmissions
# This script is called in server/src/htcondor_submit.py

condor_file=$1
output_dir_base=$2
username=$3
run_script=$4
testing=$5
login_info=$6

# script name
#nodeScript=nodeScript.sh

outDir=$output_dir_base$username
mkdir -p $outDir
cp $condor_file $outDir
cp $run_script $outDir
cp $login_info $outDir
cd $outDir

#'condor_submit',condorfile
