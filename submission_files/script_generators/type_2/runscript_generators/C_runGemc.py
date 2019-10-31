# Runs GEMC using the gcard, on LUND generated events.
#
# Input:  scard.data['genOutput']
# Output: gemc.evio
# Type 2 store the name of the gcard in the file "job.gcard"
# The variable $lundFile is passed by run.sh to this script (nodescript.sh)
# N is passed as 0 to gemc to process all events in the LUND file

def C_runGemc(scard, **kwargs):

	runGemc = """
# Run GEMC
# --------

# saving date for bookmarking purposes:
set gemcDate = `date`

# copying gcard to gemc.gcard
cp `cat job.gcard` gemc.gcard

set INPUTC=`echo -INPUT_GEN_FILE=\'lund, $lundFile\'`
echo GEMC INPUT: $INPUTC

echo
echo GEMC executable: `which gemc`
gemc -USE_GUI=0 -OUTPUT="evio, gemc.evio" -N=0 `echo $INPUTC` gemc.gcard
echo
printf "GEMC Completed on: "; /bin/date
echo
echo "Directory Content After GEMC:"
ls -l
echo

# End of GEMC
# -----------

"""

	return runGemc
