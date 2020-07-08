# Runs GEMC using the gcard, on LUND generated events.
#
# Input:  number of events, scard.data['genOutput']
# Output: gemc.evio
# Type 1 store the name of the gcard in the file "job.gcard"


def C_runGemc(scard, **kwargs):

	gemcInputOptions = ""

	if scard.genExecutable == 'gemc':
		gemcInputOptions = scard.genOptions
	else:
		gemcInputOptions = """ -INPUT_GEN_FILE="lund, {0}" """.format(scard.genOutput)


	runGemc = """
# Run GEMC
# --------

# saving date for bookmarking purposes:
set gemcDate = `date`

# copying gcard to gemc.gcard
cp `cat job.gcard` gemc.gcard

echo
echo GEMC executable: `which gemc`
gemc -USE_GUI=0 -OUTPUT="evio, gemc.evio" -N={0} {1} gemc.gcard
echo
printf "GEMC Completed on: "; /bin/date
echo
echo "Directory Content After GEMC:"
ls -l
echo

# End of GEMC
# -----------

""".format(scard.nevents, gemcInputOptions)

	return runGemc
