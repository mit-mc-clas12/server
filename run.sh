#!/bin/bash

# The SubMit Project: Container Executable Script
# Downloads the script to run in the container,
# Based on the submission ID
# -----------------------------------------------
#
# Arguments:
# 1. submission ID
# 2. subjob id (defined by the farm submission configuration file)

submissionID=$1
sjob=$2

# script name
nodeScript=nodeScript.sh

outDir="out_"$submissionID"/simu_"$sjob
mkdir -p $outDir
cd $outDir


echo
echo Downloading runscript with submissionID: $submissionID
echo

rm -f $nodeScript

# sqlite run. Assuming DB is in the same dir
sqlite3 ../../CLAS12_OCRDB.db "SELECT runscript_text FROM Submissions WHERE submissionID = $submissionID"  > $nodeScript
echo Now running $nodeScript with submissionID: $submissionID" inside directory: "`pwd`

chmod +x $nodeScript
./$nodeScript $submissionID
echo
echo $nodeScript run completed.
echo
