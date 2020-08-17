# Runs reconstruction recon-util on gemc.hipo

def E_runCooking(scard, **kwargs):

  # yaml with path

  configuration = scard.configuration
  YAMLFILE = configuration + ".yaml"

  inputFile = "gemc.hipo"

  if scard.bkmerging != 'no':

    inputFile = "gemc.merged.hipo"


  strn = """

# Run Reconstruction
# ------------------

# saving date for bookmarking purposes:
set reconstructionDate = `date`

# copying the yaml file to recon.yaml
cp /jlab/clas12Tags/$CLAS12TAG"/config/"{0} {0}

set configuration = `echo YAML file: {0}`
echo
echo
echo executing: recon-util -y {0} -i {1} -o recon.hipo
recon-util -y {0} -i {1} -o recon.hipo
echo
printf "recon-util Completed on: "; /bin/date
echo
echo "Directory Content After recon-util:"
ls -l
echo

# End of Reconstruction
# ---------------------

"""
  return strn.format(YAMLFILE, inputFile)
