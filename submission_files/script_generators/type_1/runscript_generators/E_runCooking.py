# Runs reconstruction (with clara) on gemc.hipo
#
# Input:  gemc.hipo
# Output: recon.hipo

def E_runCooking(scard, **kwargs):
  strn = """

# Run Reconstruction
# ------------------

# saving date for bookmarking purposes:
set reconstructionDate = `date`
set configuration = `echo {0} | awk -F".gcard" '{print $1}'
set YAMLFILE = $configuration".yaml"

set configuration = `echo `
echo
echo
echo executing: recon-util -y $YAMLFILE -i gemc.hipo -o recon.hipo
recon-util -y $YAMLFILE -i gemc.hipo -o recon.hipo
echo
printf "recon-util Completed on: "; /bin/date
echo
echo "Directory Content After recon-util:"
ls -l
echo

# End of Reconstruction
# ---------------------

"""
  return strn
