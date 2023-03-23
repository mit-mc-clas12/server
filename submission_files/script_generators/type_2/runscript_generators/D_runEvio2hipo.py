# Runs evio2hipo on the gemc output
# Merge background if so requested by the user
def D_runEvio2hipo(scard, **kwargs):

  torusField = scard.torus
  solenField = scard.solenoid

  evio2hipo = "echo Gemc 5.1 or later has hipo output"

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

echo "Directory Content After Background Merging:"
ls -l
if ($? != 0) then
	echo ls failure
	echo removing data files and exiting
	rm -f *.hipo *.evio
	exit 211
endif

echo "Removing background file"
rm $bgFile

echo BACKGROUNDMERGING END:  `date +%s`

# End of background merging
# ------------------------

""".format(scard.configuration, scard.fields, scard.bkmerging)

  return evio2hipo + mergeBackground
