#!/bin/bash

# utility script to copy files to jlab dir to test the condor submit
# files copied:
# 1. the latest condor file
# 2. the DB file and run.sh

scp run.sh /opt/projects/simDistribution/SubMit/utils/../utils/database/CLAS12_OCRDB.db ftp:osg

latestSub=`\ls -rt /opt/projects/simDistribution/SubMit/utils/../server/submission_files/generated_files/condor_files/ | tail -1`
echo Latest Condor Submission: $latestSub
scp /opt/projects/simDistribution/SubMit/utils/../server/submission_files/generated_files/condor_files/$latestSub ftp:osg
