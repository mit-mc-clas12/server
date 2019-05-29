# Runs GEMC using the gcard, on LUND generated events.
#
# Input:  scard.data['genOutput']
# Output: gemc.evio

def runGemc(scard, **kwargs):
  if 'https://' in scard.data.get('generator'):
    strn = """
# Run GEMC
# --------

# saving date for bookmarking purposes:
set gemcDate = `date`

echo
printf "Running events from user lund file $lundFile gcard >{0}<"
echo Executable: `which gemc`
gemc -USE_GUI=0 -OUTPUT="evio, gemc.evio" -N={0} -INPUT_GEN_FILE="lund,  $lundFile" {0}
cp {0} .
echo
printf "GEMC Completed on: "; /bin/date
echo
echo "Directory Content After GEMC:"
ls -l
echo

# End of GEMC
# -----------
""".format(kwargs.get('gcard_loc'))
  else:
    strn = """
# Run GEMC
# --------

# saving date for bookmarking purposes:
set gemcDate = `date`

echo
printf "Running {0} events with GEMC using gcard >{2}<"
echo Executable: `which gemc`
gemc -USE_GUI=0 -OUTPUT="evio, gemc.evio" -N={0} -INPUT_GEN_FILE="lund, {1}" {2}
cp {2} .
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
