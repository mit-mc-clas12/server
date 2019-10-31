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
lundFileC=$3

lundFile=${lundFileC##*/}


# script name
nodeScript=nodeScript.sh

outDir="output/simu_"$sjob
mkdir -p $outDir
cp *.* $outDir
cd $outDir


echo
echo Running inside `pwd`
echo Directory content at start:
\ls -l
echo
echo Now running $nodeScript with FarmSubmissionID: $FarmSubmissionID

chmod +x $nodeScript

if [ $# == 3 ]; then
	echo LUND filename passed by condor: $lundFile
	./$nodeScript $FarmSubmissionID $lundFile
else
	./$nodeScript $FarmSubmissionID
fi

echo
echo $nodeScript run completed.
echo
