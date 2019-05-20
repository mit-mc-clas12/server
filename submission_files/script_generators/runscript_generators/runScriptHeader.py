# Job start up:
# created first non existing sjob directory inside submissionID dir
# prints out job information

def runScriptHeader(scard,**kwargs):

	headerSTR = """
#!/bin/csh

# Run Script Header
# -----------------

set submissionID=$1

set sjob       = 1
set sjobExists = 1

while ( $sjobExists == "1" )
	if(`filetest -d $submissionID/simu_$sjob` == 0) then
		set sjobExists = 0
	else
	@ sjob += 1
end

echo
echo Running directory: $submissionID/simu_$sjob
mkdir -p $submissionID/simu_$sjob
cd       $submissionID/simu_$sjob

# saving date for bookmarking purposes:
set startDate = `date`

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
