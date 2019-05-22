# Job start up:
# created first non existing sjob directory inside submissionID dir
# prints out job information

def runScriptHeader(scard,**kwargs):

	headerSTR = """#!/bin/csh

# The SubMit Project: Container Executable Script
# -----------------------------------------------

# Run Script Header
# -----------------

set submissionID=$1

set sjob       = 1
set sjobExists = 1
set outputDir  = ""

while ( $sjobExists == "1" )
	set outputDir  = "out_"$submissionID"/simu_"$sjob
	if(`filetest -d $outputDir` == 0) then
		set sjobExists = 0
	else
		@ sjob += 1
	endif
end

echo
echo Running directory: $outputDir
mkdir -p $outputDir
cd       $outputDir

# saving date for bookmarking purposes:
set startDate = `date`

printf "Job submitted by: {0}"
printf "Job Project: {1}"
echo
printf "Job Start time: "; /bin/date
printf "Job is running on node: "; /bin/hostname
echo

echo Directory Content before starting submittion $submissionID":"
ls -l
echo

# End of Run Script Header
# ------------------------

""".format(kwargs['username'],scard.data['group'])

	return headerSTR
