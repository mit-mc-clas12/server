# Logs Job information
#
# nodeScript.sh arguments used:
# $1 submission ID
# $2 condor file transferred, including the path "lund_dir", for example lund_dir/1.txt

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
		echo $cvmfsSetupFile does not exist. Exiting
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
module load mcgen/1.6

set submissionID = $1
set lundFile     = $2

# saving date for bookmarking purposes:
set startDate = `date`

echo Running directory: `pwd`

printf "Job submitted by: {0}"
printf "Job Start time: "; /bin/date
printf "Job is running on node: "; /bin/hostname
echo

# generate-seeds.py generate

echo Directory `pwd` content before starting submissionID $submissionID":"
if ($? != 0) then
  echo ls failure
  exit 211
endif
ls -l
echo

# End of Run Script Header
# ------------------------

""".format(kwargs['username'], scard.coatjavaVersion)

	return headerSTR
