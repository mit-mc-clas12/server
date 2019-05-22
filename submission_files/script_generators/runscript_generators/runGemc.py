# Runs GEMC using the gcard, on LUND generated events.
# Logs the gcard on screen.

def runGemc(scard,**kwargs):
  strn = """

# Run GEMC
# --------

# saving date for bookmarking purposes:
set gemcDate = `date`

echo
printf "Running {0} events with GEMC using gcard >{2}<"
echo Executable: `which gemc`
gemc -USE_GUI=0 -N={0} -INPUT_GEN_FILE="lund, {1}" {2}
echo
printf "GEMC Completed on: "; /bin/date
echo
echo "Directory Content After GEMC:"
ls -l
echo

# End of GEMC
# -----------

""".format(scard.data['nevents'],scard.data['genOutput'],kwargs.get('gcard_loc'))
  return strn
