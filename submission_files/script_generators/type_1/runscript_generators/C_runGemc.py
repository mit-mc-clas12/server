# Runs GEMC using the gcard, on LUND generated events.
#
# Input:  scard.data['genOutput']
# Output: gemc.evio


def C_runGemc(scard, **kwargs):

  # if the gcard already exists at the location, copy it to "job.gcard"
  # otherwise download it from DB
  copyGCard = """
# Run GEMC
# --------

# saving date for bookmarking purposes:
set gemcDate = `date`

echo
echo Running events from user lund file: $lundFile
echo Executable: `which gemc`
if ( -f {0} ) then
	echo {0} exists, copying it here
	cp {0} job.gcard
endif""".format(kwargs.get('gcard_loc'))
#else
#	rm -f job.gcard""".format(kwargs.get('gcard_loc'))
#
#  if kwargs['using_sqlite']:
#    get_gcard = """
#    echo "{0} does not exist, using sqlite3 to retrieve it"
#  	sqlite3 CLAS12_OCRDB.db 'SELECT gcard_text FROM gcards WHERE gcardID = "$submissionID"'  > job.gcard
#  endif"""
#  if not kwargs['using_sqlite']:
#    get_gcard = """
#        echo "{0} does not exist, using mysql to retrieve it"
#      	mysql --defaults-extra-file=msql_conn.txt --execute="SELECT gcard_text FROM gcards WHERE gcardID=$submissionID;"  > job.gcard
#      endif"""


  if 'http' in scard.data.get('generator'):
    runGemc = """
echo executing: gemc -USE_GUI=0 -OUTPUT='evio, gemc.evio' -INPUT_GEN_FILE='lund,  "$lundFile"' job.gcard
gemc -USE_GUI=0 -OUTPUT='evio, gemc.evio' -INPUT_GEN_FILE='lund,  "$lundFile"' job.gcard
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
gemc -USE_GUI=0 -OUTPUT="evio, gemc.evio" -N={0} -INPUT_GEN_FILE="lund, {1}" job.gcard
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
