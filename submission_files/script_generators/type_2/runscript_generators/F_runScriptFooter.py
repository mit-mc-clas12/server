# Job finish up:
# Filtering unnecessary output
# Logs statistic, each prepended by "====" for better retrieval later

def F_runScriptFooter(scard,**kwargs):

	generator = ""
	gemc_evio = ""
	gemc_hipo = ""
	reconstruction = ""
	dst = ""

	# removing generator output if not needed
	if scard.generatorOUT == "no" and scard.genExecutable != 'gemc':
		generator = """
echo Removing generated events file
rm lund.dat
"""

	# removing gemc output if not needed
	if scard.gemcEvioOUT == "no":
		gemc_evio = """
echo Removing gemc evio file
rm gemc.evio
"""

	# removing gemc decoded hipo if not needed
	if scard.gemcHipoOUT == "no":
		gemc_hipo = """
echo Removing gemc hipo file
rm gemc.hipo
rm gemc.merged.hipo
rm 0*.hipo
"""

	# creating the DST if requested
	if scard.dstOUT == "yes":
		dst = """
echo Creating the DST
hipo-utils -filter -b 'RUN::*,RAW::epics,RAW::scaler,HEL::flip,HEL::online,REC::*,RECFT::*,MC::*' -merge -o dst.hipo recon.hipo
"""

	# removing reconstruction output
	if scard.reconstructionOUT == "no":
		reconstruction = """
echo Removing reconstructed file
rm recon.hipo
	"""

	strn = """
# Removing Unnecessary Files and Creating DST if selected
# -------------------------------------------------------

{0}
{1}
{2}
{3}
{4}

# Run Script Footer
# -----------------

set endDate = `date`

echo ==== SubMit-Job === Job Start: $startDate
echo ==== SubMit-Job === Generator Start: $generatorDate
echo ==== SubMit-Job === GEMC Start: $gemcDate
echo ==== SubMit-Job === evio2hipoDate Start: $evio2hipoDate
echo ==== SubMit-Job === Reconstruction Start: $reconstructionDate
echo ==== SubMit-Job === Job End: $endDate

# End of Run Script Footer
# ------------------------

"""

	return strn.format(generator, gemc_evio, gemc_hipo, dst, reconstruction)
