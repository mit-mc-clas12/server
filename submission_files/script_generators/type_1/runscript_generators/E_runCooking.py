# Runs reconstruction on gemc.hipo
#
# Input:  gemc.hipo
# Output: recon.hipo

def E_runCooking(scard,**kwargs):
  strn = """

# Run Reconstruction
# ------------------

# saving date for bookmarking purposes:
set reconstructionDate = `date`

echo
echo
echo executing: notsouseful-util -i gemc.hipo -o recon.hipo -c 2
notsouseful-util -i gemc.hipo -o recon.hipo -c 2
echo
printf "notsouseful-util Completed on: "; /bin/date
echo
echo "Directory Content After notsouseful-util:"
ls -l
echo

# End of Reconstruction
# ---------------------

"""
  return strn
