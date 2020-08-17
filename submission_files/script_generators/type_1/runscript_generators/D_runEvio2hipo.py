# Runs evio2hipo on the gemc output
# To read files from xrootd:
# setenv LD_PRELOAD /usr/lib64/libXrdPosixPreload.so
def D_runEvio2hipo(scard, **kwargs):

  torusField = scard.torus
  solenField = scard.solenoid

  evio2hipo = """

# Run evio2hipo
# -------------

# saving date for bookmarking purposes:
set evio2hipoDate = `date`

echo
printf "Running evio2hipo with torus current scale: {0} and solenoid current scale: {1}"
echo
echo
echo executing: evio2hipo -r 11 -t {0} -s {1} -i gemc.evio -o gemc.hipo
evio2hipo -r 11 -t {0} -s {1} -i gemc.evio -o gemc.hipo
echo
printf "evio2hipo Completed on: "; /bin/date
echo
echo "Directory Content After evio2hipo:"
ls -l
echo

# End of evio2hipo
# ----------------

""".format(torusField, solenField, scard.configuration, scard.fields, scard.bkmerging)


  mergeBackground = ""

  if scard.bkmerging != 'no':

    mergeBackground = """

# Run background merging
# ----------------------

echo "Directory Content Before Background Merging:"
ls -l

bgMerginFilename.sh {0} {1} {2} get

set bgFile = `ls 0*.hipo`

echo xrootd file to load: $bgFile

bg-merger -b $bgFile -i gemc.hipo -o gemc.merged.hipo -d "DC,FTOF,HTCC,ECAL"

echo "Directory Content After Background Merging:"
ls -l

# End ofbackground merging
# ------------------------

""".format(scard.configuration, scard.fields, scard.bkmerging)

  return evio2hipo + mergeBackground
