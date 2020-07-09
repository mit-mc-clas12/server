# Runs reconstruction (with clara) on gemc.hipo
#
# Input:  gemc.hipo
# Output: recon.hipo

def E_runCooking(scard, **kwargs):

  # gcard with path

  configuration = scard.configuration
  YAMLFILE = configuration + ".yaml"

  strn = """

# Run Reconstruction
# ------------------

# saving date for bookmarking purposes:
set reconstructionDate = `date`

set configuration = `echo YAML file: {0}`
echo
echo
echo executing: recon-util -y {0} -i gemc.hipo -o recon.hipo
recon-util -y {0} -i gemc.hipo -o recon.hipo
echo
printf "recon-util Completed on: "; /bin/date
echo
echo "Directory Content After recon-util:"
ls -l
echo

# End of Reconstruction
# ---------------------

"""
  return strn.format(YAMLFILE)
