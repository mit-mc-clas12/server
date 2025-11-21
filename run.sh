#!/bin/bash

# The SubMit Project: Container Executable Script
# -----------------------------------------------
#
# Arguments:
# 1. submission ID
# 2. subjob id (defined by the farm submission configuration file)
# 3. (optional) lund filename for types 2 and 4. This is passed by the condor file

FarmSubmissionID=$1
sjob=$2
lundFile=$3

# script name
nodeScript=nodeScript.sh

outDir="output"
mkdir -p $outDir
cp *.* $outDir
cd $outDir


echo
echo Running inside `pwd`
echo Directory content at start:
\ls -l
echo

chmod +x $nodeScript

if [ $# == 3 ]; then
	echo "Now running nodeScript with options FarmSubmissionID: "$FarmSubmissionID",  lundFile: " $lundFile
	./$nodeScript $FarmSubmissionID $lundFile $sjob
	exit $?
else
	echo "Now running nodeScript with options FarmSubmissionID: "$FarmSubmissionID
	./$nodeScript $FarmSubmissionID $sjob
	exit $?
fi

