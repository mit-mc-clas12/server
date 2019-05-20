#****************************************************************
"""
# Commentary for this file does not yet exist
"""
#****************************************************************

def runCooking(scard,**kwargs):
  strn = """

# Run Reconstruction
# ------------------

# saving date for bookmarking purposes:
set reconstructionDate = `date`

echo
printf "Running notsouseful-util with torus current scale: {0} and solenoid current scale: {1}"
echo
echo
notsouseful-util -i gemc.hipo -o out_gemc.hipo -c 2
echo
printf "notsouseful-util Completed on: "; /bin/date
echo
printf "Directory Content After notsouseful-util:"
ls -l
echo

# End of Reconstruction
# ---------------------

"""
  return strn
