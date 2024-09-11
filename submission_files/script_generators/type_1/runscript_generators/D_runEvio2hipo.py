# Runs evio2hipo on the gemc output
# Merge background if so requested by the user
def D_runEvio2hipo(scard, **kwargs):
    torusField = scard.torus
    solenField = scard.solenoid

    inputFileForDenoiser = "gemc.hipo"

    if scard.bkmerging != 'no':
        inputFileForDenoiser = "gemc.merged.hipo"

    evio2hipo = "echo Gemc 5.1 or later has hipo output, no need to run evio2hipo"

    if scard.gemcv == '4.4.2':
        evio2hipo = """

# Run evio2hipo
# -------------

echo EVIO2HIPO START:  `date +%s`

echo
printf "Running evio2hipo with torus current scale: {0} and solenoid current scale: {1}"
echo
echo
echo executing: evio2hipo -r 11 -t {0} -s {1} -i gemc.evio -o gemc.hipo
evio2hipo -r 11 -t {0} -s {1} -i gemc.evio -o gemc.hipo
if ($? != 0) then
	echo evio2hipo failed.
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 205
endif

echo
printf "evio2hipo Completed on: "; /bin/date
echo
echo Removing evio file
rm -f gemc.evio
echo
echo "Directory Content After evio2hipo:"
ls -l
if ($? != 0) then
	echo ls failure
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 211
endif

echo EVIO2HIPO END:  `date +%s`

# End of evio2hipo
# ----------------

""".format(torusField, solenField, scard.configuration, scard.fields, scard.bkmerging)

    mergeBackground = ""

    if scard.bkmerging != 'no':
        mergeBackground = """

# Run background merging
# ----------------------

echo BACKGROUNDMERGING START:  `date +%s`

bg-merger -b $bgFile -i gemc.hipo -o gemc.merged.hipo -d "DC,FTOF,ECAL,HTCC,LTCC,BST,BMT,CND,CTOF,FTCAL,FTHODO"

if ($? != 0) then
	echo bg-merger failed.
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 206
endif

echo Removing background file and original hipo file
rm -f gemc.hipo $bgFile
echo 
echo "Directory Content After Background Merging:"
ls -l
if ($? != 0) then
	echo ls failure
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 211
endif

echo BACKGROUNDMERGING END:  `date +%s`

# End of background merging
# ------------------------

""".format(scard.configuration, scard.fields, scard.bkmerging)

    # temp exiting here for testing
    denoiser = "echo Gemc 4.4.2 does not run the de-noiser, skipping it; "

    if scard.gemcv != '4.4.2':
        denoiser = """
  
# Run de-noiser
# -------------

echo DE-NOISING START:  `date +%s`

$DRIFTCHAMBERS/install/bin/denoise2.exe  -i {0} -o gemc_denoised.hipo -t 1 -n $DRIFTCHAMBERS/denoising/code/network/cnn_autoenc_0f_112.json 

if ($? != 0) then
	echo de-noiser failed.
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 230
endif

echo Removing original hipo file {0}
rm -f {0}
echo "Directory Content After de-noiser:"
ls -l
if ($? != 0) then
	echo ls failure
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 211
endif

echo DE-NOISING END:  `date +%s`

# End of de-noiser
# ----------------


""".format(inputFileForDenoiser)

    return evio2hipo + mergeBackground + denoiser
