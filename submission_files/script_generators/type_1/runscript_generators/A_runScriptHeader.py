# Logs Job information
#
# nodeScript.sh arguments used:
# $1 submission ID

def A_runScriptHeader(scard, **kwargs):

	headerSTR = """#!/bin/csh

# The SubMit Project: Container Script "nodeScript.sh", downloaded from DB and executed by run.sh
# ===============================================================================================
#
# Run Script Header
# -----------------

source /etc/profile.d/environment.csh

set submissionID=$1

# saving date for bookmarking purposes:
set startDate = `date`

echo Running directory: `pwd`

printf "Job submitted by: {0}"
printf "Job Project: {1}"
echo
printf "Job Start time: "; /bin/date
printf "Job is running on node: "; /bin/hostname
echo

echo Directory `pwd` content before starting submissionID $submissionID":"
ls -l
echo

# End of Run Script Header
# ------------------------

""".format(kwargs['username'], scard.data['group'])
	
	return headerSTR
