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

  strHeader = """# The SubMit Project: Condor Type 1 Submission Script
# --------------------------------------------

Universe = vanilla

# singularity image and CVMFS binding
+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/jeffersonlab/clas12software:{0}"
+SingularityBindCVMFS = True

#Rank = (GLIDEIN_SITE=?='CNAF') || (GLIDEIN_SITE=?='SGridGLA')
Rank = ( (GLIDEIN_SITE=?='CNAF') || (GLIDEIN_SITE=?='SGridGLA') || (GLIDEIN_SITE=?='Lamar-Cluster') ) ? 200 : ((GLIDEIN_SITE=?='SU-ITS') ? 0 : 100)

# Retry automatically
on_exit_remove   = (ExitBySignal == False) && (ExitCode == 0)
on_exit_hold     = (ExitBySignal == True) || (ExitCode != 0)
periodic_release = (NumJobCompletions < 5) && ((CurrentTime - EnteredCurrentStatus) > (60*60)) && ((exit==202) || (exit ==204) || (exit ==205) || (exit ==206) || (exit ==207) || (exit ==208) || (exit ==210) || (exit ==211) || (exit ==212) || (exit ==213))

""".format(scard.submission)

  # OSG Farm Requirements
  requirementsStr = """
# OSG Requirements
Requirements = (HAS_SINGULARITY =?= TRUE) && (HAS_CVMFS_oasis_opensciencegrid_org=?=True) && (OSG_HOST_KERNEL_VERSION >= 21700) && (CVMFS_oasis_opensciencegrid_org_REVISION >= 16688) && (OSG_GLIDEIN_VERSION >= 534)

+UNDESIRED_Sites = ""KSU""
+UNDESIRED_Sites = ""FNAL_GPGrid""
"""

  return strHeader + requirementsStr
