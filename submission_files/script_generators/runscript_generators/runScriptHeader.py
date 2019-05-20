# Job start up: prints out job information

def runScriptHeader(scard,**kwargs):

	headerSTR = """
#!/bin/csh

# Run Script Header
# -----------------

set submissionID=$1

printf "Job submitted by: {0}"
printf "Job Project: {1}"
echo
printf "Job Start time: "; /bin/date
printf "Job is running on node: "; /bin/hostname
echo

printf "Directory Content before starting submittion $submissionID:"
ls -l
echo

# End of Run Script Header
# ------------------------

""".format(kwargs['username'],scard.data['group'])

	return headerSTR
