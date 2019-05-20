#!/bin/bash

gcardID=$1

nodeScript=nodeScript.sh

echo
echo Downloading runscript with GCARD ID: $gcardID
echo

rm -f $nodeScript
sqlite3 ../utils/database/CLAS12_OCRDB.db "SELECT runscript_text FROM Submissions WHERE GcardID = $gcardID"  > $nodeScript

echo $nodeScript downloaded with content:
echo
cat $nodeScript
echo
echo Now running $nodeScript

chmod +x $nodeScript
#./$nodeScript $gcardID
echo
echo $nodeScript run completed.
