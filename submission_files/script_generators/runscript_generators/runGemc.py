# Runs GEMC using the gcard, on LUND generated events.
#
# Input:  scard.data['genOutput']
# Output: gemc.evio

import ntpath

# the gcard is already loaded into job.card by run.sh

def runGemc(scard, **kwargs):

  # if the gcard already exists at the location, copy it to "job.gcard"
  # otherwise download it from DB
  copyGCard = """
# Run GEMC
# --------

# saving date for bookmarking purposes:
set gemcDate = `date`

echo
printf "Running events from user lund file $lundFile"
echo Executable: `which gemc`

if ( -f {0} ) then
   echo {0} exists, copying it here
	cp {0} job.gcard
else
	echo {0} does not exist, using sqlite to get it with command SELECT gcard_text FROM gcards WHERE gcardID = $submissionID
	sqlite3 CLAS12_OCRDB.db "SELECT gcard_text FROM gcards WHERE gcardID = $submissionID"  > job.gcard
endif
""".format(kwargs.get('gcard_loc'))


  if 'https://' in scard.data.get('generator'):
    runGemc = """

gemc -USE_GUI=0 -OUTPUT="evio, gemc.evio" -N={0} -INPUT_GEN_FILE="lund,  $lundFile" job.gcard


echo
printf "GEMC Completed on: "; /bin/date
echo
echo "Directory Content After GEMC:"
ls -l
echo

# End of GEMC
# -----------
"""
  else:
    runGemc = """
# Run GEMC
# --------

# saving date for bookmarking purposes:
set gemcDate = `date`

echo
printf "Running {0} events with GEMC using gcard >{2}<"
echo Executable: `which gemc`
gemc -USE_GUI=0 -OUTPUT="evio, gemc.evio" -N={0} -INPUT_GEN_FILE="lund, {1}" job.gcard
cp {2} .
echo
printf "GEMC Completed on: "; /bin/date
echo
echo "Directory Content After GEMC:"
ls -l
echo

# End of GEMC
# -----------

""".format(scard.data['nevents'],scard.data['genOutput'])

  # copyGCard and runGemc
  return copyGCard + runGemc
