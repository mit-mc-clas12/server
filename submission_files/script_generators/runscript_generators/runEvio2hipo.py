#****************************************************************
"""
# Commentary for this file does not yet exist
"""
#****************************************************************

def runEvio2hipo(scard,**kwargs):
  strn = """

# Run evio2hipo
# -------------

# saving date for bookmarking purposes:
set evio2hipoDate = `date`

echo
printf "Running evio2hipo with torus current scale: {0} and solenoid current scale: {1}"
echo
echo
evio2hipo -r 11 -t {0} -s {1} -i out.ev -o gemc.hipo
echo
printf "evio2hipo Completed on: "; /bin/date
echo
echo "Directory Content After evio2hipo:"
ls -l
echo

# End of evio2hipo
# ----------------

""".format(scard.data['tcurrent'],scard.data['pcurrent'])
  return strn
