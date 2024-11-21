# Runs GEMC using the gcard, on LUND file produced by generator
#
#
# N is set to to the number requested by the user, with a max of 10K set by the portal

def C_runGemc(scard, **kwargs):

	gemcInputOptions = """ -INPUT_GEN_FILE="lund, {0}" """.format(scard.genOutput)
	gemcAdditionalOptions = """ -INTEGRATEDRAW="*" """.format(scard.genOutput)
	redirectOutput = """ \| sed "/G4Exception-START/,/G4Exception-END/d"  """

	submission_type = "prod"
	if scard.submission == "devel":
		submission_type = "dev"

	c12f_home = f'/cvmfs/oasis.opensciencegrid.org/jlab/hallb/clas12/sw/noarch/clas12-config/{submission_type}/'
	gcard = c12f_home + "gemc/" + scard.gemcv + "/" + scard.configuration + ".gcard"

	if scard.genExecutable == 'gemc':
		gemcInputOptions = scard.genOptions

	torusField = """ -SCALE_FIELD="binary_torus,    {0}" """.format(scard.torus)
	solenField = """ -SCALE_FIELD="binary_solenoid, {0}" """.format(scard.solenoid)

	output = """ -OUTPUT="hipo, gemc.hipo" """
	all_vertex_options = """  """

	if scard.gemcv == '4.4.2':
		output = """ -OUTPUT="evio, gemc.evio" """
		torusField = """ -SCALE_FIELD="TorusSymmetric,     {0}" """.format(scard.torus)
		solenField = """ -SCALE_FIELD="clas12-newSolenoid, {0}" """.format(scard.solenoid)
	else:
		vertex_z = """ -RANDOMIZE_LUND_VZ="{0}" """.format(scard.vertex_z_to_gemc)
		beamspot = """ -BEAM_SPOT="{0}"         """.format(scard.beamspot_to_gemc)
		raster   = """ -RASTER_VERTEX="{0}"     """.format(scard.raster_to_gemc)

		if 'n/a' in scard.vertex_z_to_gemc:
			vertex_z = ''
		if 'n/a' in scard.beamspot_to_gemc:
			beamspot = ''
		if 'n/a' in scard.raster_to_gemc:
			raster = ''

		all_vertex_options = vertex_z + beamspot + raster

	runGemc = """
# Run GEMC
# --------

echo GEMC START:  `date +%s`

echo
echo GEMC executable: 
which gemc
echo gcard: {0}
echo
ls ../

gemc -USE_GUI=0 -NGENP=100 -N={1} {0} {2} {3} {4} {5} {6} {7} {8}
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
echo "Removing LUND file"
rm -f {9}
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

""".format(gcard, scard.nevents, gemcInputOptions, all_vertex_options, torusField, solenField, output, gemcAdditionalOptions, redirectOutput, scard.genOutput)

	return runGemc
