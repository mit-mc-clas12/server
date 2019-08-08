# Job start up:
# - creates first non existing sjob directory inside submissionID dir
# - screen logs job information
#
# Arguments:
# 1. submission ID
# 2. lundfile if present

def A_runScriptHeader(scard, **kwargs):

	headerSTR = """#!/bin/csh

# The SubMit Project: Container Script, downloaded from DB and executed by run.sh
# -------------------------------------------------------------------------------

# Run Script Header
# -----------------

source /etc/profile.d/environmentB.csh

set submissionID=$1

# lund file is passed as an argument to this script
# in condor this process is automatic. Assuming in other farm it is as well
set lundFile=$2

# saving date for bookmarking purposes:
set startDate = `date`

echo Running directory: `pwd`

printf "Job submitted by: {0}"
printf "Job Project: {1}"
echo
printf "Job Start time: "; /bin/date
printf "Job is running on node: "; /bin/hostname
echo

echo Directory `pwd` content before starting submission $submissionID":"
ls -l
echo

# End of Run Script Header
# ------------------------

""".format(kwargs['username'], scard.data['group'])

	return headerSTR
