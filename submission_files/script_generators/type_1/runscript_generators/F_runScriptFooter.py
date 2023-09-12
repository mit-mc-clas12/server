# Job finish up:
# Removing unnecessary output

def F_runScriptFooter(scard,**kwargs):

	dst = ""

	# creating the DST if requested
	if scard.dstOUT == "yes":
		dst = """
echo
echo Creating the DST
echo
hipo-utils -filter -b 'RUN::*,RAW::epics,RAW::scaler,HEL::flip,HEL::online,REC::*,RECFT::*,MC::RecMatch,MC::GenMatch,MC::Particle,MC::User,MC::Header,MC::Lund,MC::Event' -merge -o dst.hipo recon.hipo
if ($? != 0) then
  echo hipo-utils failed, removing data files and exiting
  rm -f *.hipo *.evio
  exit 208
endif

echo
printf "DST Completed on: "; /bin/date
echo
echo "Directory Content After DST:"
ls -l
if ($? != 0) then
	echo ls failure
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 211
endif
echo
echo
echo Simulation + Reconstruction Successfully Completed on: `date +%s` 
"""


	strn = """
# Removing Unnecessary Files and Creating DST if selected
# -------------------------------------------------------

{0}

echo Additional cleanup
rm -f core* *.gcard
rm -f recon.hipo gemc.hipo gemc.merged.hipo gemc_denoised.hipo 
rm -f run.sh nodeScript.sh condor_exec.exe
rm -f RNDMSTATUS random-seeds.txt {1}

echo
echo nodeScript run completed.
echo "Final Directory Content:"
ls -l
echo

# End of Run Script Footer
# ------------------------

	"""

	return strn.format(dst, scard.genOutput)
