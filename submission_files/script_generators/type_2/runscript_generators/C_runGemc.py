# Runs GEMC using the gcard, on LUND generated events.
#
# The variable $lundFile is passed by run.sh to this script (nodescript.sh)
# N is set to 10,000 to gemc to process the max allowed number of events

def C_runGemc(scard, **kwargs):






	torusField = """ -SCALE_FIELD="binary_torus,    {0}" """.format(scard.torus)
	solenField = """ -SCALE_FIELD="binary_solenoid, {0}" """.format(scard.solenoid)

	output = """ -OUTPUT="hipo, gemc.hipo" """
	if scard.gemcv == '4.4.2':
		output = """ -OUTPUT="evio, gemc.evio" """
		torusField = """ -SCALE_FIELD="TorusSymmetric,     {0}" """.format(scard.torus)
		solenField = """ -SCALE_FIELD="clas12-newSolenoid, {0}" """.format(scard.solenoid)

	runGemc = """
# Run GEMC
# --------

echo GEMC START:  `date +%s`

# copying the gcard to <conf>.gcard
cp $GEMC/../config/"{0}".gcard" {0}.gcard

echo
echo GEMC executable: `which gemc`

gemc -USE_GUI=0 {3} -N=10000 -INPUT_GEN_FILE="lund, lund.dat" {0}.gcard  {1} {2}
if ($? != 0) then
	echo gemc failed
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 204
endif
# removing generated events file
rm -f *.dat

echo
printf "GEMC Completed on: "; /bin/date
echo
echo "Directory Content After GEMC:"
ls -l
if ($? != 0) then
	echo ls failure
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 211
endif
echo

echo GEMC END:  `date +%s`

# End of GEMC
# -----------

""".format(scard.configuration, torusField, solenField, output)

	return runGemc
