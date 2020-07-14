#!/bin/bash

# For HTCondor FarmSubmissions
# This script is called in server/src/htcondor_submit.py

scripts_baseDir=$1
jobOutputDir=$2
username=$3
# hardcoding this, not sure how to pass it 
submissionID=$4
url=$5
dbType=$6
dbName=$7

outDir=$jobOutputDir"/"$username"/job_"$submissionID


mkdir -p $outDir
cd $outDir
rm -rf *
mkdir -p log

cp $scripts_baseDir/server/run.sh .


# Downloading files for the run

rm -f clas12.condor nodeScript.sh job.gcard

echo $dbName

if [ "$dbType" = "Test SQLite DB" ] ; then
    sqlite3 "$dbName" "SELECT clas12_condor_text FROM submissions WHERE user_submission_id=$submissionID;" | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' | sed s/\'\'/\"/g > clas12.condor
    sqlite3 "$dbName" "SELECT runscript_text FROM submissions WHERE user_submission_id=$submissionID;"     | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' > nodeScript.sh
    sqlite3 "$dbName" "SELECT scard FROM submissions where user_submission_id=$submissionID;"    | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' | grep gcards | awk '{print $2}' > job.gcard
elif [ "$dbType" = "Test MySQL DB" ] ; then
    cp $scripts_baseDir/msql_conn_test.txt .
    mysql --defaults-extra-file=msql_conn_test.txt -N -s --execute="SELECT clas12_condor_text FROM submissions WHERE user_submission_id=$submissionID;" | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' | sed s/\'\'/\"/g > clas12.condor
    mysql --defaults-extra-file=msql_conn_test.txt -N -s --execute="SELECT runscript_text FROM submissions WHERE user_submission_id=$submissionID;"     | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' > nodeScript.sh
    mysql --defaults-extra-file=msql_conn_test.txt -N -s --execute="SELECT scard from CLAS12OCR.submissions where user_submission_id=$submissionID;"    | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' | grep gcards | awk '{print $2}' > job.gcard
elif [ "$dbType" = "Production MySQL DB" ] ; then
    cp $scripts_baseDir/msql_conn.txt .
    mysql --defaults-extra-file=msql_conn.txt -N -s --execute="SELECT clas12_condor_text FROM submissions WHERE user_submission_id=$submissionID;" | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' | sed s/\'\'/\"/g > clas12.condor
    mysql --defaults-extra-file=msql_conn.txt -N -s --execute="SELECT runscript_text FROM submissions WHERE user_submission_id=$submissionID;"     | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' > nodeScript.sh
    mysql --defaults-extra-file=msql_conn.txt -N -s --execute="SELECT scard from CLAS12OCR.submissions where user_submission_id=$submissionID;"    | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' | grep gcards | awk '{print $2}' > job.gcard
else
    echo "Error, database type not recognized in condor_submit.sh"
    echo $dbType
fi




# Get lund files and send job 
python $scripts_baseDir/server/lund_downloader.py --url=$url --output_dir='lund_dir'
condor_submit clas12.condor 2> condorSubmissionError.txt

# Clean up 
rm msql_conn.txt

