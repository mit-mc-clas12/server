# Runs evio2hipo on the gemc output
#
# Input:  gemc.evio
# Output: gemc.hipo

def D_runEvio2hipo(scard, **kwargs):

  gcard = scard.data['gcards']
  lim = gcard.find(".")
  configuration = gcard[0:lim]


  strn = """

# Run evio2hipo
# -------------

# saving date for bookmarking purposes:
set evio2hipoDate = `date`


set configuration = {0} 


set torusField = -1
set solenField = 1

if ($configuration == "rgk-fall2018") then
	echo rgk fall 2018 has inverted torus polarity
	set torusField = 1
endif

echo
printf "Running evio2hipo with torus current scale:  $torusField and solenoid current scale: $solenField"
echo
echo
echo executing: evio2hipo -r 11 -t $torusField -s $solenField -i gemc.evio -o gemc.hipo
evio2hipo -r 11 -t $torusField -s $solenField -i gemc.evio -o gemc.hipo
echo
printf "evio2hipo Completed on: "; /bin/date
echo
echo "Directory Content After evio2hipo:"
ls -l
echo

# End of evio2hipo
# ----------------

""".format(configuration)
  return strn
