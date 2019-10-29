# Type 2 has no generator, events are from a lund file
#
# Input:  scard.data['genExecutable']
def B_runGenerator(scard,**kwargs):

  strGeneratorHeader = """
# Generator
# ---------

echo
echo LUND Event File: {0}
echo

# End of Run Generator
# ---------------------

""".format(scard.data['genExecutable'])

  return strGeneratorHeader
