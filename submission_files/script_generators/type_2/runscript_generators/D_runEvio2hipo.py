# Runs evio2hipo on the gemc output
# To read files from xrootd:
# setenv LD_PRELOAD /usr/lib64/libXrdPosixPreload.so
def D_runEvio2hipo(scard, **kwargs):

  torusField = scard.torus
  solenField = scard.solenoid

  strn = """

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



# Run background merging
# ----------------------

echo "Directory Content Before Background Merging:"
ls -l

setenv LD_PRELOAD /usr/lib64/libXrdPosixPreload.so

echo xrootd file to load:

ls xroot://sci-xrootd-ib//osgpool/hallb/clas12/backgroundfiles/{2}/{3}/{4}/10k

unsetenv LD_PRELOAD

echo "Directory Content After Background Merging:"
ls -l


# End ofbackground merging
# ------------------------

""".format(torusField, solenField, scard.configuration, scard.fields, scard.bkmerging)
  return strn
