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

FarmSubmissionID=$1
sjob=$2
lundFile=$3

# script name
nodeScript=nodeScript.sh

outDir="out_"$FarmSubmissionID"/simu_"$sjob
mkdir -p $outDir
cp *.txt $outDir
cd $outDir


echo
echo Running inside `pwd`
echo Directory content at start:
\ls -l
echo
echo Downloading runscript with FarmSubmissionID: $FarmSubmissionID
echo

rm -f $nodeScript

# mysql run to download the running script and the gcard.
/bin/mysql --defaults-extra-file=msql_conn.txt -N -s --execute="SELECT runscript_text FROM FarmSubmissions WHERE FarmSubmissionID=$FarmSubmissionID;" | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' > $nodeScript
echo
echo Content of $nodeScript
echo
cat $nodeScript
echo
echo End of $nodeScript
echo
echo Now running $nodeScript with FarmSubmissionID: $FarmSubmissionID

chmod +x $nodeScript

if [ $# == 3 ]; then
	echo LUND filename: $lundFile
	./$nodeScript $FarmSubmissionID $lundFile
else
	./$nodeScript $FarmSubmissionID
fi

echo
echo $nodeScript run completed.
echo
