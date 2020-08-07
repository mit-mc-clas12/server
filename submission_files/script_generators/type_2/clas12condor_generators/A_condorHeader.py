# Condor Submission Script Header
#
# Individual farms requirements
#
# farm_name possible choices:
#
# Note:to submit to MIT_Tier2 add:
# Requirements  = (GLIDEIN_Site == "MIT_CampusFactory" && BOSCOGroup == "bosco_lns")
#
# Note:to bind to CVMFS add:
# +SingularityBindCVMFS = True

def A_condorHeader(scard, **kwargs):

  strHeader = """# The SubMit Project: Condor Type 2 Submission Script
# --------------------------------------------

Universe = vanilla

# singularity image and CVMFS binding
+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/jeffersonlab/clas12software:{0}"
+SingularityBindCVMFS = True

""".format(scard.submission)

  # OSG Farm Requirements
  requirementsStr = """
# OSG Requirements
Requirements = HAS_SINGULARITY == TRUE
"""

  return strHeader + requirementsStr
