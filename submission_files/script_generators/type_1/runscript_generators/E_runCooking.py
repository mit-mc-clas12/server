# Runs reconstruction recon-util

def E_runCooking(scard, **kwargs):

	submission_type = "prod"
	if scard.submission == "devel":
		submission_type = "dev"

	c12f_home = f'/cvmfs/oasis.opensciencegrid.org/jlab/hallb/clas12/sw/noarch/clas12-config/{submission_type}/'
	yaml = c12f_home + "coatjava/" + scard.coatjavav + "/" + scard.configuration + ".yaml"

	inputFileForCooking = "gemc_denoised.hipo"

	if scard.gemcv == '4.4.2':
		inputFileForCooking = "gemc.merged.hipo"

		if scard.bkmerging == 'no':
			inputFileForCooking = "gemc.hipo"

	strn = """

# Run Reconstruction
# ------------------

echo RECONSTRUCTION START:  `date +%s`

echo content of yaml file {0}:
cat {0}

echo
df /cvmfs/oasis.opensciencegrid.org && df . && df /tmp
if ($? != 0) then
	echo df failure
	echo removing data files and exiting
    rm -f *.hipo *.evio *.sqlite
	exit 213
endif

echo
echo executing: recon-util -y {0} -i {1} -o recon.hipo -- -Xmx2560m
recon-util -y {0} -i {1} -o recon.hipo -- -Xmx2560m

if ($? != 0) then
	echo recon-util failed.
	echo removing data files and exiting
    rm -f *.hipo *.evio *.sqlite
	exit 207
endif
df /cvmfs/oasis.opensciencegrid.org && df . && df /tmp
if ($? != 0) then
	echo df failure
	echo removing data files and exiting
    rm -f *.hipo *.evio *.sqlite
	exit 213
endif

echo
printf "recon-util Completed on: "; /bin/date
echo
echo "Directory Content After recon-util:"
ls -l
if ($? != 0) then
	echo ls failure
	echo removing data files and exiting
    rm -f *.hipo *.evio *.sqlite
	exit 211
endif

echo executing: hipo-utils -test recon.hipo
hipo-utils -test recon.hipo
if ($? != 0) then
	echo hipo-utils failure
	echo removing data files and exiting
    rm -f *.hipo *.evio *.sqlite
	exit 214
endif

if (`stat -L -c%s recon.hipo` < 100) then
	echo hipo size failure
	echo removing data files and exiting
    rm -f *.hipo *.evio *.sqlite
	exit 215
endif

echo
echo RECONSTRUCTION END:  `date +%s`
echo

# End of Reconstruction
# ---------------------

"""

	return strn.format(yaml, inputFileForCooking)
