# Logs Job information
#
# nodeScript.sh arguments used:
# $1 submission ID
# $2 condor file transferred, including the path "lund_dir", for example lund_dir/1.txt

def A_runScriptHeader(scard, **kwargs):

	headerSTR = """#!/bin/csh

# Run Script Header
# -----------------

source /etc/profile.d/environment.csh
setenv RCDB_CONNECTION mysql://null

set submissionID = $1
set lundFile     = $2

# saving date for bookmarking purposes:
set startDate = `date`

echo Running directory: `pwd`

printf "Job submitted by: {0}"
printf "Job Start time: "; /bin/date
printf "Job is running on node: "; /bin/hostname
echo

echo Directory `pwd` content before starting submissionID $submissionID":"
ls -l
echo

# End of Run Script Header
# ------------------------

""".format(kwargs['username'])

	return headerSTR
