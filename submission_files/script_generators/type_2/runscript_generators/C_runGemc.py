# Runs GEMC using the gcard, on LUND generated events.
#
# The variable $lundFile is passed by run.sh to this script (nodescript.sh)
# N is passed as 0 to gemc to process all events in the LUND file

def C_runGemc(scard, **kwargs):






	torusField = scard.torus
	solenField = scard.solenoid

	runGemc = """
# Run GEMC
# --------

# saving date for bookmarking purposes:
set gemcDate = `date`

# copying the gcard to <conf>.gcard
cp /jlab/clas12Tags/$CLAS12TAG"/config/"{0}".gcard" {0}.gcard

echo
echo GEMC executable: `which gemc`

echo "Directory Content before GEMC"
ls -l

gemc -USE_GUI=0 -OUTPUT="evio, gemc.evio" -N=10000 -INPUT_GEN_FILE="lund, lund.dat" {0}.gcard  -SCALE_FIELD="TorusSymmetric, {1}" -SCALE_FIELD="clas12-newSolenoid, {2}"
if ($? != 1) then
  echo gemc failed.
  exit 204
endif

echo
printf "GEMC Completed on: "; /bin/date
echo
echo "Directory Content After GEMC:"
ls -l
if ($? != 0) then
  echo ls failure
  exit 211
endif
echo

# End of GEMC
# -----------

""".format(scard.configuration, torusField, solenField)

	return runGemc
