#!/bin/bash

# For HTCondor FarmSubmissions
# This script is called in server/src/htcondor_submit.py

scripts_baseDir=$1
jobOutputDir=$2
username=$3
# hardcoding this, not sure how to pass it 
submissionID=$4

outDir=$jobOutputDir"/"$username"/out_"$submissionID


mkdir -p $outDir
cd $outDir
rm -f *
mkdir log

cp $scripts_baseDir/server/run.sh .
cp $scripts_baseDir/msql_conn.txt .

# Downloading files for the run
rm -f clas12.condor nodeScript.sh job.gcard
mysql --defaults-extra-file=msql_conn.txt -N -s --execute="SELECT clas12_condor_text FROM FarmSubmissions WHERE FarmSubmissionID=$submissionID;" | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' > clas12.condor
mysql --defaults-extra-file=msql_conn.txt -N -s --execute="SELECT runscript_text FROM FarmSubmissions WHERE FarmSubmissionID=$submissionID;"     | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' > nodeScript.sh
mysql --defaults-extra-file=msql_conn.txt -N -s --execute="SELECT gcard_text FROM gcards WHERE gcardID=$submissionID;"                           | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' > job.gcard

condor_submit clas12.condor
