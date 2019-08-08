# Condor Submission Script Header Maker
# Header
# Individual farms requirements
#
# farm_name possible choices:
#
# MIT_Tier2
# OSG

def A_condorHeader(scard, **kwargs):
  farm_name = scard.data.get('farm_name')

  strHeader = """# The SubMit Project: Condor Submission Script
# --------------------------------------------

Universe = vanilla

# singularity image and CVMFS binding
+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/jeffersonlab/clas12simulations:production"
+SingularityBindCVMFS = True
"""

  # OSG Farm Requirements
  requirementsStr = """
# OSG Requirements
Requirements = HAS_SINGULARITY == TRUE
"""
  # MIT Farm Requirements
  if farm_name == 'MIT_Tier2':
	  requirementsStr = """
Requirements  = (GLIDEIN_Site == "MIT_CampusFactory" && BOSCOGroup == "bosco_lns")
"""

  return strHeader + requirementsStr
