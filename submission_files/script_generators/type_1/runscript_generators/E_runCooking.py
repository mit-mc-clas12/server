# Runs reconstruction recon-util on gemc.hipo

import os

def E_runCooking(scard, **kwargs):

  # yaml with path
  coatjava=os.environ.get('COATJAVA')
  YAMLFILE=coatjava + "/config/mc.yaml"
  MOD_YAML="yes"

  clas12_dir=os.environ.get('GEMC') + "/" + "../config/"

  if scard.gemcv == '4.4.2':
    configuration = scard.configuration
    YAMLFILE = clas12_dir + configuration + ".yaml"
    MOD_YAML="yes"

  inputFile = "gemc.hipo"

  if scard.bkmerging != 'no':

    inputFile = "gemc.merged.hipo"


  strn = """

# Run Reconstruction
# ------------------

echo RECONSTRUCTION START:  `date +%s`

# copying the yaml file to mc.yaml
cp {0} mc.yaml

set configuration = `echo YAML file: mc.yaml`
if ({2} == "yes") then
	
endif

cat mc.yaml
echo
df /cvmfs/oasis.opensciencegrid.org && df . && df /tmp
if ($? != 0) then
	echo df failure
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 213
endif

echo
echo executing: recon-util -y mc.yaml -i {1} -o recon.hipo
recon-util -y mc.yaml -i {1} -o recon.hipo
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
  return strn.format(YAMLFILE, inputFile, MOD_YAML)
