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

#echo trying to save subID to temp file

#echo $submissionID > subID_file

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
#echo mysql -u $mysql_user -p $mysql_pass
#mysql --defaults-extra-file=msqlconf.txt --execute="SELECT runscript_text FROM Submissions WHERE submissionID = $submissionID;"  > $nodeScript
#mysql --defaults-extra-file=msql_conn.txt -N -s --execute='SELECT runscript_text FROM Submissions WHERE submissionID = $submissionID;'  > $nodeScript
#echo about to enter csh
#csh
#set subID=`cat subID_file`
#mysql --defaults-extra-file=msql_conn.txt  -N -s --execute='SELECT runscript_text FROM Submissions WHERE submissionID = 3;'  |  awk '{gsub(/\\n/,"\n")}1' > $nodeScript

mysql --defaults-extra-file=msql_conn.txt -N -s --execute="SELECT runscript_text FROM Submissions WHERE submissionID=$submissionID;" | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1' > $nodeScript
#mysql --defaults-extra-file=msql_conn.txt -N -s --execute="SELECT runscript_text FROM Submissions WHERE submissionID=$submissionID;" > test$submissionID.txt
#set msql_out=`mysql --defaults-extra-file=msql_conn.txt -N -s --execute='SELECT runscript_text FROM Submissions WHERE submissionID = $subID;'`
#echo $msql_out > $nodeScript
#exit
echo Now running $nodeScript with submissionID: $submissionID" inside directory: "`pwd`



if [ $# == 3 ]; then
	echo LUND filename: $lundFile
fi

chmod +x $nodeScript
./$nodeScript $submissionID $lundFile
echo
echo $nodeScript run completed.
echo