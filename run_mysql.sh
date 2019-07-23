#!/bin/bash

# The SubMit Project: Container Executable Script
# Downloads the script to run in the container,
# Based on the submission ID
# -----------------------------------------------
#
# Arguments:
# 1. submission ID
# 2. subjob id (defined by the farm submission configuration file)
# 3. (optional) lund file

submissionID=$1
sjob=$2
lundFile=$3

# script name
nodeScript=nodeScript.sh

outDir="out_"$submissionID"/simu_"$sjob
mkdir -p $outDir
cp *.txt $outDir
cd $outDir


echo
echo Directory content at start: `\ls -l`
echo
echo Downloading runscript with submissionID: $submissionID
echo

rm -f $nodeScript

# mysql run to download the running script and the gcard.
mysql --defaults-extra-file=msql_conn.txt -N -s --execute="SELECT runscript_text FROM Submissions WHERE submissionID=$submissionID;" | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' > $nodeScript
echo
echo
echo Content of $nodeScript
echo
cat $nodeScript
echo
echo end of $nodeScript
echo
echo Now running $nodeScript with submissionID: $submissionID" inside directory: "`pwd`

chmod +x $nodeScript

if [ $# == 3 ]; then
echo LUND filename: $lundFile
./$nodeScript $submissionID $lundFile
else
./$nodeScript $submissionID
fi

echo
echo $nodeScript run completed.
echo
