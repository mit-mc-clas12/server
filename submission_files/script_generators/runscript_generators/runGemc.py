#****************************************************************
"""
# Commentary for this file does not yet exist
"""
#****************************************************************

def runGemc(scard,**kwargs):
  strn = """

# Run GEMC
# --------

echo
printf "Running {0} events with GEMC using gcard >{2}<."
echo Content of gcard:
echo
cat {2}
echo
gemc -USE_GUI=0 -N={0} -INPUT_GEN_FILE="lund, {1}" {2}
echo
printf "GEMC Completed on: "; /bin/date
echo
printf "Directory Content After GEMC:"
ls -l
echo

# End of GEMC
# -----------

""".format(scard.data['nevents'],scard.data['genOutput'],kwargs.get('gcard_loc'))
  return strn
