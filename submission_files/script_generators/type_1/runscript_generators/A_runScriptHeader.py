# writes nodeScript.sh header
#
# arguments used:
#
# $1 submission ID


def A_runScriptHeader(scard, **kwargs):

	c12f_home = "/cvmfs/oasis.opensciencegrid.org/jlab/hallb/clas12/sw/noarch/clas12-config/dev/"
	gcard = c12f_home + "gemc/" + scard.gemcv + "/" + scard.configuration + ".gcard"
	yaml = c12f_home + "coatjava/" + scard.coatjavav + "/" + scard.configuration + ".yaml"

	modified_conf = scard.configuration

	if modified_conf == "rga_fall2018_target_at_m3.5" :
		modified_conf = "rga_fall2018"

	headerSTR = """#!/bin/csh

echo SCRIPTHEADER START:  `date +%s`
printf "Job is running on node: "; /bin/hostname
printf "Job submitted by: {0}"
echo Running directory: `pwd`
set submissionID=$1
set sjobID=$2
echo Directory `pwd` content before starting submissionID $submissionID":"
ls -l
if ($? != 0) then
  echo ls failure
  exit 211
endif

# Run Script Header
# -----------------
set echo
# limit core size
# ulimit -c 10

# clearing module environment, as suggested by OSG, #67051
unsetenv ENABLE_LMOD
unsetenv _LMFILES_
unsetenv LMOD_ANCIENT_TIME
unsetenv LMOD_arch
unsetenv LMOD_CMD
unsetenv LMOD_COLORIZE
unsetenv LMOD_DEFAULT_MODULEPATH
unsetenv LMOD_DIR
unsetenv LMOD_FULL_SETTARG_SUPPORT
unsetenv LMOD_PACKAGE_PATH
unsetenv LMOD_PKG
unsetenv LMOD_PREPEND_BLOCK
unsetenv LMOD_SETTARG_CMD
unsetenv LMOD_SETTARG_FULL_SUPPORT
unsetenv LMOD_sys
unsetenv LMOD_SYSTEM_DEFAULT_MODULES
unsetenv LMOD_VERSION
unsetenv LOADEDMODULES
unsetenv MODULEPATH
unsetenv MODULEPATH_ROOT
unsetenv MODULESHOME

# Exit if cvmfs file not found, source it if found
# ------------------------------------------------

source /etc/profile.d/modules.csh
set cvmfsPath = /cvmfs/oasis.opensciencegrid.org/jlab/hallb/clas12/sw/
set cvmfsSetupFile = $cvmfsPath/setup.csh
if (-f $cvmfsSetupFile ) then
		echo $cvmfsSetupFile exists, sourcing it with path $cvmfsPath
		source $cvmfsSetupFile $cvmfsPath
		set cvmfsSetupFile2 = /cvmfs/oasis.opensciencegrid.org/jlab/geant4/ceInstall/geant4_cvmfs.csh 
		if (-f $cvmfsSetupFile2 ) then
			echo $cvmfsSetupFile1 exists, sourcing it
			source $cvmfsSetupFile2 
		else
			echo CVMFS ERROR $cvmfsSetupFile2 does not exist. Exiting
			exit 202
		endif
endif
else
		echo CVMFS ERROR $cvmfsSetupFile does not exist. Exiting
		exit 202
endif
if ( ! -f {6} ) then
	echo gcard not found, exiting
	exit 241
endif
if ( ! -f {7} ) then
	echo yaml not found, exiting
	exit 242
endif

module unload gemc
module unload coatjava
module unload jdk
module unload root
module unload mcgen
module load sqlite/{1}
module unload ccdb
module load gemc/{1}

# TODO: RCDB_CONNECTION currently not used. When fixed, remove this line.
setenv RCDB_CONNECTION mysql://null

module avail
module load coatjava/{2}
module load jdk/{3}
#module load root/{4}
module load mcgen/{5}

echo ROOT Version: {4}
echo MCGEN Version: {5}
echo SQLITE Version: {1}
echo GEMC Version: {1}
echo JDK Version: {3}
echo COATJAVA Version: {2}




echo
echo
echo SCRIPTHEADER END:  `date +%s`
echo

# End of Run Script Header
# ------------------------

""".format(kwargs['username'], scard.gemcv, scard.coatjavav,  scard.jdkv, scard.rootv, scard.mcgenv, gcard, yaml)

	fetchBackgroundFile = ""

	if scard.bkmerging != 'no':

		fetchBackgroundFile = """

# Fetch background merging
# ------------------------

echo FETCHBACKGROUNDFILE START:  `date +%s`

/bin/bgMerginFilename.sh {0} {1} {2} get

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

echo FETCHBACKGROUNDFILE END:  `date +%s`

# End ofbackground Merging Fetch
# ------------------------------

""".format(modified_conf, scard.fields, scard.bkmerging)

	return headerSTR + fetchBackgroundFile
