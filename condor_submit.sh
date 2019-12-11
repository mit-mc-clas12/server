#!/bin/bash

# For HTCondor FarmSubmissions
# This script is called in server/src/htcondor_submit.py

scripts_baseDir=$1
jobOutputDir=$2
username=$3
# hardcoding this, not sure how to pass it 
submissionID=$4
url=$5

outDir=$jobOutputDir"/"$username"/job_"$submissionID


mkdir -p $outDir
cd $outDir
rm -rf *
mkdir -p log

cp $scripts_baseDir/server/run.sh .
cp $scripts_baseDir/msql_conn.txt .

# Downloading files for the run
rm -f clas12.condor nodeScript.sh job.gcard
mysql --defaults-extra-file=msql_conn.txt -N -s --execute="SELECT clas12_condor_text FROM submissions WHERE user_submission_id=$submissionID;" | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' | sed s/\'\'/\"/g > clas12.condor
mysql --defaults-extra-file=msql_conn.txt -N -s --execute="SELECT runscript_text FROM submission WHERE user_submission_id=$submissionID;"     | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' > nodeScript.sh
#mysql --defaults-extra-file=msql_conn.txt -N -s --execute="SELECT gcard_text FROM Gcards WHERE GcardID=$submissionID;"                           | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' > job.gcard


# Get lund files and send job 
python $scripts_baseDir/server/lund_downloader.py --url=$url --output_dir='lund_dir'
condor_submit clas12.condor 2> condorSubmissionError.txt

# Clean up 
rm msql_conn.txt

