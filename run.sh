#!/bin/bash

# Need to pass argumenet from HTCondor to right here (change Gcard = 1 to Gcard = variable_name)
echo `sqlite3 CLAS12_OCRDB.db "SELECT runscript_text FROM Submissions WHERE GcardID = 1" ` >> runscript.sh
chmod +x runscript.sh
./runscript.sh
