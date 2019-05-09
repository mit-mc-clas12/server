#****************************************************************
"""
# Commentary for this file does not yet exist
"""
#****************************************************************

def startup(scard,**kwargs):

  strn1 = """set ClusterId = ` awk -F '=' '/^ClusterId/ {print $2}' $PWD/.job.ad`"""
  strn2 = """set ProcId = ` awk -F '=' '/^ProcId/ {print $2}' $PWD/.job.ad`"""

  strn ="""#!/bin/csh\n
set script_start  = `date`\n
# source /cvmfs/cms.cern.ch/cmsset_default.csh\n
echo "XXXXXXXXXXXX"
#cat $PWD/.job.ad
echo "XXXXXXXXXXXX"
echo Submitted by {0}, {1}\n
uname -a\n
echo " ==== PWD"
pwd\n
echo " ==== ./"
ls -lhrt ./\n
echo " ==== /etc/profile.d/"
ls -lhrt /etc/profile.d/\n
echo " ==== ENV"
env\n
source /etc/profile.d/environmentB.csh
cd /tmp\n
#set ClusterId = `sed -n '0,/ClusterId = "\([^"]*\)"/\1/p' $PWD/.job.ad`\n
{2}
echo ClusterId $ClusterId\n
{3}
echo ProcId $ProcId\n""".format(kwargs['username'],scard.data['group'],strn1,strn2)
  return strn
