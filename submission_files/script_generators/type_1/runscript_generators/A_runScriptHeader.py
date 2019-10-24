# Logs Job information
#
# nodeScript.sh arguments used:
# $1 submission ID
#
# TODO: some nodes come with XERCESROOT defined. This is fixed here but it will be addressed in the container environment

def A_runScriptHeader(scard, **kwargs):

	headerSTR = """#!/bin/csh

# The SubMit Project: Container Script "nodeScript.sh", downloaded from DB and executed by run.sh
# ===============================================================================================
#
# Run Script Header
# -----------------

setenv XERCESROOT /jlab/2.3/Linux_CentOS7.5.1804-x86_64-gcc4.8.5/xercesc/3.2.2
setenv XERCESC_VERSION 3.2.2

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

""".format(kwargs['username'], scard.data['group_name'])
	
	return headerSTR
