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
cp CLAS12_OCRDB.db $outDir
cp *.txt $outDir
cd $outDir

echo
echo Running inside `pwd`
echo Directory content at start:
\ls -l
echo
echo Downloading runscript with submissionID: $submissionID
echo

rm -f $nodeScript

# sqlite run to download the running script and the gcard. Assuming DB is in the same dir
sqlite3 CLAS12_OCRDB.db "SELECT runscript_text FROM FarmSubmissions WHERE submissionID = $submissionID"  > $nodeScript
echo
echo Content of $nodeScript
echo
cat $nodeScript
echo
echo End of $nodeScript
echo
echo Now running $nodeScript with submissionID: $submissionID

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
