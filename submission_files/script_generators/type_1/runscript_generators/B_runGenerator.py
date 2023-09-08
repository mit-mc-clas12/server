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
echo GENERATOR START:  `date +%s`

# generate-seeds.py is in the path
generate-seeds.py generate


set seed = `generate-seeds.py read --row 1`
echo Generator seed from generate-seeds, row 1: $seed

echo
echo Running {1} events with generator {0} with options: {2} 
echo Generator:
which {0}
echo
{0} --trig {1} --docker {2} --seed $seed

if ($? != 0) then
  echo GENERATOR ERROR ">"{0}"<" failed.
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

echo GENERATOR END:  `date +%s`

# End of Run Generator
# ---------------------

""".format(scard.genExecutable, scard.nevents, scard.genOptions)

    return strGeneratorHeader
