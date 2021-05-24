# Job finish up:
# Removing unnecessary output

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
rm -f {1}

echo
echo nodeScript run completed.
echo

# End of Run Script Footer
# ------------------------

	"""

	return strn.format(dst, scard.genOutput)
