#****************************************************************
"""
# Commentary for this file does not yet exist
"""
#****************************************************************

def initialization(scard,**kwargs):
  strn = """\nprintf "Start time: "; /bin/date
printf "Job is running on node: "; /bin/hostname
printf "Job running as user: "; /usr/bin/id
printf "Job is running in directory: "; /bin/pwd\n
echo
echo JLAB_ROOT: $JLAB_ROOT
echo\n
echo starting files
ls -l
set generator_start  = `date`
{0} --trig {1} --docker {2}
echo after generator""".format(scard.data['genExecutable'],scard.data['nevents'],scard.data['genOptions'])
  return strn
