# Type 2 has no generator, events are from a lund file
#
# The  $lundFile is copied to the harcoded name lund.dat because
# of quotes complications (conversion double to single due to mysql)

def B_runGenerator(scard,**kwargs):

  strGeneratorHeader = """
# Generator
# ---------

setenv XDG_RUNTIME_DIR /run/user/6635
setenv BEARER_TOKEN_FILE /var/run/user/6635/bt_u6635

echo
echo Running pelican object get $lundFile lund.dat
pelican object get $lundFile lund.dat
echo

# End of Run Generator
# ---------------------

"""

  return strGeneratorHeader
