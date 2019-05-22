#!/bin/bash

submissionID=$1
mkdir -p $submissionID

nodeScript=nodeScript.sh

echo
echo Downloading runscript with submissionID: $submissionID
echo

rm -f $nodeScript

# sqlite run. Assuming DB is in the same dir
sqlite3 CLAS12_OCRDB.db "SELECT runscript_text FROM Submissions WHERE submissionID = $submissionID"  > $nodeScript

echo Now running $nodeScript with submissionID: $submissionID

chmod +x $nodeScript
./$nodeScript $submissionID
echo
echo $nodeScript run completed.
