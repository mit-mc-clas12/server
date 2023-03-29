# Runs reconstruction recon-util on gemc.hipo

import os
 
def E_runCooking(scard, **kwargs):

  LOCALYAML = 'mc.yaml'
  
  YAMLFILE  = 'mc.yaml'
  
  MC_YAML = "yes"

  inputFile = "gemc.hipo"
  gcard = scard.configuration + ".gcard"

  if scard.gemcv == '4.4.2':
    YAMLFILE = scard.configuration + ".yaml"
    MC_YAML="no"


  if scard.bkmerging != 'no':
    inputFile = "gemc.merged.hipo"

  dum="'{print $2}'"

  strn = """

# Run Reconstruction
# ------------------

echo RECONSTRUCTION START:  `date +%s`


if ({2} == "yes") then
   cp $COATJAVA/config/{0} {3}
   set DIGI_VARIATION = `grep DIGI {4} | awk -Fvalue {5} | awk -F\" {5} `
	echo " adding DIGI_VARIATION = $DIGI_VARIATION to {3} "
   sed -i s/configuration:/"configuration:\n  global:\n    variation: $DIGI_VARIATION"/g  {3}
else
   cp $GEMC/../config/{0} {3}
endif

echo content of yaml file {3}:
cat {3}

echo
df /cvmfs/oasis.opensciencegrid.org && df . && df /tmp
if ($? != 0) then
	echo df failure
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 213
endif

echo
echo executing: recon-util -y {3} -i {2} -o recon.hipo
recon-util -y {3} -i {1} -o recon.hipo
if ($? != 0) then
	echo recon-util failed.
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 207
endif
df /cvmfs/oasis.opensciencegrid.org && df . && df /tmp
if ($? != 0) then
	echo df failure
	echo removing data files and exiting
	rm -f *.hipo *.evio
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
	rm -f *.hipo *.evio
	exit 211
endif

hipo-utils -test recon.hipo
if ($? != 0) then
	echo hipo-utils failure
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 214
endif

if (`stat -L -c%s recon.hipo` < 100) then
	echo hipo size failure
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 215
endif

echo RECONSTRUCTION END:  `date +%s`

# End of Reconstruction
# ---------------------

"""
  return strn.format(YAMLFILE, inputFile, MC_YAML, LOCALYAML, gcard, dum)
