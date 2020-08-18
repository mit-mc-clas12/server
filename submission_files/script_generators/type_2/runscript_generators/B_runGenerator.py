# Type 2 has no generator, events are from a lund file
#
# The  $lundFile is copied to the harcoded name lund.dat because
# of quotes complications (conversion double to single due to mysql)

def B_runGenerator(scard,**kwargs):

  strGeneratorHeader = """
# Generator
# ---------

echo
echo LUND Event File: $lundFile
mv $lundFile lund.dat
echo

# End of Run Generator
# ---------------------

"""

  return strGeneratorHeader
