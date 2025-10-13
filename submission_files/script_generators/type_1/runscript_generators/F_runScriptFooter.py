# Job finish up:
# Removing unnecessary output

def F_runScriptFooter(scard,**kwargs):

	dst = "echo DST not requested: {0}".format(scard.dstOUT)

	# creating the DST if requested
	if scard.dstOUT == "yes":
		dst = """
echo
echo Creating the DST
echo
hipo-utils -filter -b 'RUN::*,RAW::epics,RAW::scaler,HEL::flip,HEL::online,REC::*,RECFT::*,MC::RecMatch,MC::GenMatch,MC::Particle,MC::User,MC::Header,MC::Lund,MC::Event' -merge -o dst.hipo recon.hipo
set outputFileName="{0}"$submissionID"-"$sjobID".hipo"
echo submissionID is $submissionID
echo sjobID is $sjobID
echo outputFileName is $outputFileName
echo Moving the DST to the output file $outputFileName
mv dst.hipo $outputFileName
if ($? != 0) then
  echo hipo-utils failed, removing data files and exiting
  rm -f *.hipo *.evio *.sqlite
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
    rm -f *.hipo *.evio *.sqlite
	exit 211
endif
echo
echo
echo DST Successfully created on: `date +%s` 

""".format(scard.user_string)


	strn = """

{0}

# Running Pelican

echo _CONDOR_CREDS: $_CONDOR_CREDS
setenv BEARER_TOKEN_FILE "$_CONDOR_CREDS/jlab_clas12.use"
echo " BEARER_TOKEN_FILE: $BEARER_TOKEN_FILE"
echo " pelican: " `which pelican`
echo " pelican ls /volatile for {2}: "
pelican object ls osdf:///jlab-osdf/clas12/volatile/{2}
echo Running pelican on: $outputFileName
 
# running pelican
echo pelicon output to osdf:///jlab-osdf/clas12/volatile/osg/{2}/$sjobID/$outputFileName
/usr/bin/pelican -d object put $outputFileName osdf:///jlab-osdf/clas12/volatile/osg/{2}/$sjobID/$outputFileName
echo Additional cleanup
rm -f core* *.gcard
rm -f recon.hipo gemc.hipo gemc.merged.hipo gemc_denoised.hipo 
rm -f run.sh nodeScript.sh condor_exec.exe
rm -f RNDMSTATUS random-seeds.txt {1}
rm -f gemc.evio
rm -f *.hipo 

echo
echo nodeScript run completed.
echo "Final Directory Content:"
ls -l
echo

# End of Run Script Footer
# ------------------------

	"""

	return strn.format(dst, scard.genOutput, kwargs['username'])
