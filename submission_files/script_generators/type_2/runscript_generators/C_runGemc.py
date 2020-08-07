# Runs GEMC using the gcard, on LUND generated events.
#
# The variable $lundFile is passed by run.sh to this script (nodescript.sh)
# N is passed as 0 to gemc to process all events in the LUND file

def C_runGemc(scard, **kwargs):

	runGemc = """
# Run GEMC
# --------

# saving date for bookmarking purposes:
set gemcDate = `date`

# copying the gcard to gemc.gcard
cp /jlab/clas12Tags/$CLAS12TAG/config/{0}.gcard gemc.gcard

echo
echo GEMC executable: `which gemc`
gemc -USE_GUI=0 -OUTPUT="evio, gemc.evio" -N=0 -INPUT_GEN_FILE="lund, lund.dat" gemc.gcard
echo
printf "GEMC Completed on: "; /bin/date
echo
echo "Directory Content After GEMC:"
ls -l
echo

# End of GEMC
# -----------

""".format(scard.configuration)

	return runGemc
