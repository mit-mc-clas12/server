#****************************************************************
"""
# Commentary for this file does not yet exist
"""
#****************************************************************

def condor_startup(scard,**kwargs):
  #CHANGE THIS ONCE FUNCTION IS PROPERLY IMPLEMENTED
  farm_name = scard.data.get('farm_name')
  strn_osg = """# The UNIVERSE defines an execution environment. You will almost always use vanilla.
Universe = vanilla\n
# singularity image
Requirements = HAS_SINGULARITY == TRUE
+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/jeffersonlab/clas12simulations:production"
+SingularityBindCVMFS = True
"""

  strn_submit = """# The UNIVERSE defines an execution environment. You will almost always use vanilla.
Universe = vanilla\n
+SINGULARITY_JOB = true
+SINGULARITY_SHELL = csh\n
# singularity image\n
Requirements  = (GLIDEIN_Site == "MIT_CampusFactory" && BOSCOGroup == "bosco_lns")
+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/jeffersonlab/clas12simulations:production"
+SingularityBindCVMFS = True
"""
  if farm_name == 'osg':
    return strn_osg
  elif farm_name == 'MIT_Tier2' or farm_name == 'ifarm':
    return strn_submit
  else:
    return "farm could not be found, inspect scard"
