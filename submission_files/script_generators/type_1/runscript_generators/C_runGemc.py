# Runs GEMC using the gcard, on LUND generated events.
#
# Input:  number of events, scard.data['genOutput']
# Output: gemc.evio


def C_runGemc(scard, **kwargs):

	runGemc = """
# Run GEMC
# --------

# saving date for bookmarking purposes:
set gemcDate = `date`


echo
echo GEMC executable: `which gemc`
gemc -USE_GUI=0 -OUTPUT="evio, gemc.evio" -N={0} -INPUT_GEN_FILE="lund, {1}" job.gcard
echo
printf "GEMC Completed on: "; /bin/date
echo
echo "Directory Content After GEMC:"
ls -l
echo

# End of GEMC
# -----------

""".format(scard.data['nevents'], scard.data['genOutput'])

	return runGemc
