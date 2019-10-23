# Runs evio2hipo on the gemc output
#
# Input:  gemc.evio
# Output: gemc.hipo

def D_runEvio2hipo(scard, **kwargs):

  gcard = scard.data['gcards'].split('/')[-1]
  lim = gcard.find(".")
  configuration = gcard[0:lim]

  torusField = -1
  solenField = -1

  if configuration == "rgk-fall2018":
    torusField = 1


  strn = """

# Run evio2hipo
# -------------

# saving date for bookmarking purposes:
set evio2hipoDate = `date`


echo
printf "Running evio2hipo with torus current scale:  $torusField and solenoid current scale: $solenField"
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

""".format(torusField, solenField)
  return strn
