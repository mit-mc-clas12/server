#!/bin/bash

submissionID=$1
mkdir -p $submissionID

nodeScript=nodeScript.sh

echo
echo Downloading runscript with GCARD ID: $submissionID
echo

rm -f $nodeScript
sqlite3 ../utils/database/CLAS12_OCRDB.db "SELECT runscript_text FROM Submissions WHERE submissionID = $submissionID"  > $nodeScript

echo $nodeScript downloaded with content:
echo
cat $nodeScript
echo
echo Now running $nodeScript

chmod +x $nodeScript
./$nodeScript $submissionID
echo
echo $nodeScript run completed.
