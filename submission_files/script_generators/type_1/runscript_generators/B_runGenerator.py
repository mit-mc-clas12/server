# Runs the chosen generator with its options

def B_runGenerator(scard, **kwargs):

    strGeneratorHeader = ""

    if scard.genExecutable == 'gemc':
        strGeneratorHeader = """
# Generator
# ---------
#
# gemc internal
#
# End of Run Generator
# ---------------------
"""

    else:
        strGeneratorHeader = """
# Generator
# ---------

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

""".format(scard.genExecutable, scard.nevents, scard.genOptions)

    return strGeneratorHeader
