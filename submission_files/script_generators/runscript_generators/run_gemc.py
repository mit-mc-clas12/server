#****************************************************************
"""
# Commentary for this file does not yet exist
"""
#****************************************************************

def run_gemc(scard,**kwargs):
  strn = """\n\nls -l
set gemc_start = `date`
gemc -USE_GUI=0 -N={0} -INPUT_GEN_FILE="lund, {1}" {2} {3}
echo after gemc\n""".format(scard.data['nevents'],scard.data['genOutput'],scard.data['luminosity'],kwargs.get('gcard_loc'))
  return strn
