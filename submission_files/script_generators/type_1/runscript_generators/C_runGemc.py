# Runs GEMC using the gcard, on LUND file produced by generator
#
#
# N is set to to the number requested by the user, with a max of 10K set by the portal

def C_runGemc(scard, **kwargs):

	gemcInputOptions = """ -INPUT_GEN_FILE="lund, {0}" """.format(scard.genOutput)

	if scard.genExecutable == 'gemc':
		gemcInputOptions = scard.genOptions

	torusField = """ -SCALE_FIELD="binary_torus,    {0}" """.format(scard.torus)
	solenField = """ -SCALE_FIELD="binary_solenoid, {0}" """.format(scard.solenoid)

	output = """ -OUTPUT="hipo, gemc.hipo" """
	all_vertex_options = " -USE_GUI=0 "

	if scard.gemcv == '4.4.2':
		output = """ -OUTPUT="evio, gemc.evio" """
		torusField = """ -SCALE_FIELD="TorusSymmetric,     {0}" """.format(scard.torus)
		solenField = """ -SCALE_FIELD="clas12-newSolenoid, {0}" """.format(scard.solenoid)
	else:
		vertex_z = """ -RANDOMIZE_LUND_VZ="vertex, {0}" """.format(scard.vertex_z_to_gemc)
		beamspot = """ -BEAM_SPOT="beam,           {0}" """.format(scard.beamspot_to_gemc)
		raster   = """ -RASTER_VERTEX="raster,     {0}" """.format(scard.raster_to_gemc)
		all_vertex_options = vertex_z + beamspot + raster

	runGemc = """
# Run GEMC
# --------

echo GEMC START:  `date +%s`

# copying the gcard to <conf>.gcard
cp $GEMC/../config/{2}.gcard {2}.gcard

echo
echo GEMC executable: `which gemc`

gemc -USE_GUI=0 {5} -N={0} {1} {2}.gcard {3} {4} {5}
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

""".format(scard.nevents, gemcInputOptions, scard.configuration, torusField, solenField, output, all_vertex_options)

	return runGemc
