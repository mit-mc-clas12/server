# Runs the chosen generator with options

def runGenerator(scard,**kwargs):
  if 'https://' in scard.data.get('generator'):
    strn = """
# Custom LUND file specified, not running generator
    """
  else:
    strn = """

# Run Generator
# -------------

# saving date for bookmarking purposes:
set generatorDate = `date`

echo
printf "Running {1} events with generator >{0}< with options: {2}"
echo
{0} --trig {1} --docker {2}
echo
printf "Events Generator Completed on: "; /bin/date
echo
echo "Directory Content After Generator:"
ls -l
echo

# End of Run Generator
# ---------------------

""".format(scard.data['genExecutable'],scard.data['nevents'],scard.data['genOptions'])
  return strn
