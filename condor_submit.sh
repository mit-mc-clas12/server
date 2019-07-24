#!/bin/bash

# For HTCondor FarmSubmissions
# This script is called in server/src/htcondor_submit.py

condor_file_path=$1
clas12condor_file_name=$2
output_dir_base=$3
username=$4
run_script=$5
testing=$6

# script name
#nodeScript=nodeScript.sh

outDir=$output_dir_base"/"$username
mkdir -p $outDir
cp $condor_file_path $outDir
cp $run_script $outDir
cd $outDir


if [ "$testing" == "True" ]; then
   submission="THIS IS A FAKE SUBMISSION...  3 job(s) submitted to cluster 7334290."
   echo $submission
else
  condor_submit clas12condor_file_name
fi
