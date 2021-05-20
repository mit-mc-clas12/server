# Logs Job information
#
# nodeScript.sh arguments used:
# $1 submission ID


def A_runScriptHeader(scard, **kwargs):

	headerSTR = """#!/bin/csh

# Run Script Header
# -----------------
set echo
# limit core size
ulimit -c 10

# Exit if cvmfs not found
# -----------------
set cvmfsSetupFile = /cvmfs/oasis.opensciencegrid.org/jlab/hallb/clas12/soft/setup.csh
if (-f $cvmfsSetupFile ) then
		echo $cvmfsSetupFile exists
else
		echo CVMFS ERROR $cvmfsSetupFile does not exist. Exiting
		exit 202
endif

source /etc/profile.d/environment.csh
setenv RCDB_CONNECTION mysql://null

# numbers are hardcoded currently.
# In the future we could have uber modules

module unload coatjava
module unload jdk
module unload root
module unload mcgen

module load coatjava/{1}
module load jdk/1.8.0_31
module load root/6.22.06
module load mcgen/1.9

set submissionID=$1


# saving date for bookmarking purposes:
set startDate = `date`

echo Running directory: `pwd`

printf "Job submitted by: {0}"
printf "Job Start time: "; /bin/date
printf "Job is running on node: "; /bin/hostname
echo

generate-seeds.py generate

echo Directory `pwd` content before starting submissionID $submissionID":"
ls -l
if ($? != 0) then
  echo ls failure
  exit 211
endif

echo

# End of Run Script Header
# ------------------------

""".format(kwargs['username'], scard.coatjavaVersion)


	fetchBackgroundFile = ""

	if scard.bkmerging != 'no':

		fetchBackgroundFile = """

# Fetch background merging
# ------------------------

echo "Directory Content Before Background Merging Fetch:"
ls -l

bgMerginFilename.sh {0} {1} {2} get

if ($? != 0) then
	echo bgMerginFilename failure
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 212
endif


set bgFile = `ls 0*.hipo`

if (-f $bgFile ) then
	echo xrootd file to load: $bgFile
else
	echo XROOTD ERROR: Background file $bgFile does not exist. Exiting
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 210
endif

echo "Directory Content After Background Merging Fwetch:"
ls -l
if ($? != 0) then
	echo ls failure
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 211
endif

# End ofbackground Merging Fetch
# ------------------------------

""".format(scard.configuration, scard.fields, scard.bkmerging)

	return headerSTR + fetchBackgroundFile
