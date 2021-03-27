# Job finish up:
# Filtering unnecessary output
# Logs statistic, each prepended by "====" for better retrieval later

def F_runScriptFooter(scard,**kwargs):

	dst = ""

	# creating the DST if requested
	if scard.dstOUT == "yes":
		dst = """
echo Creating the DST
hipo-utils -filter -b 'RUN::*,RAW::epics,RAW::scaler,HEL::flip,HEL::online,REC::*,RECFT::*,MC::*' -merge -o dst.hipo recon.hipo
if ($? != 0) then
  echo hipo-utils failed.
  exit 208
endif

"""


	strn = """
# Removing Unnecessary Files and Creating DST if selected
# -------------------------------------------------------

{0}

echo Additional cleanup
rm -f core*
rm -f *.gcard
rm -f recon.hipo
rm -f gemc.hipo
rm -f gemc.merged.hipo
rm -f *.evio
rm -f *.yaml
rm -f run.sh
rm -f nodeScript.sh
rm -f condor_exec.exe
rm -f RNDMSTATUS
rm -f random-seeds.txt
rm -f lund.dat


# Run Script Footer
# -----------------

set endDate = `date`

echo ==== SubMit-Job === Job Start: $startDate
echo ==== SubMit-Job === GEMC Start: $gemcDate
echo ==== SubMit-Job === evio2hipoDate Start: $evio2hipoDate
echo ==== SubMit-Job === Reconstruction Start: $reconstructionDate
echo ==== SubMit-Job === Job End: $endDate

echo
echo nodeScript run completed.
echo

# End of Run Script Footer
# ------------------------

	"""

	return strn.format(dst, scard.genOutput)
