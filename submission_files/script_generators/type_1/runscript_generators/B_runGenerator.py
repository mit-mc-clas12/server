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
# saving date for bookmarking purposes:
set generatorDate = `date`

# End of Run Generator
# ---------------------
"""

    else:
        strGeneratorHeader = """
# Generator
# ---------

# saving date for bookmarking purposes:
set generatorDate = `date`
set seed = `generate-seeds.py read --row 1`
echo Generator seed from generate-seeds, row 1: $seed

echo
printf "Running {1} events with generator >{0}< with options: {2} "
echo
{0} --trig {1} --docker {2} --seed $seed

if ($? != 0) then
  echo generator >{0}< failed.
  exit 203
endif

# removing any root file that was created
rm -f *.root

echo
printf "Events Generator Completed on: "; /bin/date
echo
echo "Directory Content After Generator:"
ls -l
if ($? != 0) then
  echo ls failure
  exit 211
endif
echo

# End of Run Generator
# ---------------------

""".format(scard.genExecutable, scard.nevents, scard.genOptions)

    return strGeneratorHeader
