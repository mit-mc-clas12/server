#****************************************************************
"""
# Commentary for this file does not yet exist
"""
#****************************************************************

def condor_1(scard,**kwargs):
  strn = """request_cpus = {0}
request_memory = {1} GB

# EXECUTABLE is the program your job will run It"s often useful
# to create a shell script to "wrap" your actual work.
Executable = {2}

# Error and Output are the error and output channels from your job
# Log is job"s status, success, and resource consumption.
Error  = log/job.$(Cluster).$(Process).err
Output = log/job.$(Cluster).$(Process).out
Log    = log/job.$(Cluster).$(Process).log

# Send the job to Held state on failure.
# on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)

# Periodically retry the jobs every 1 hour, up to a maximum of 5 retries.
# periodic_release =  (NumJobStarts < 5) && ((CurrentTime - EnteredCurrentStatus) > 60*60)

# default CLAS12 project
+ProjectName = "{3}"
""".format(scard.data['cores_req'],scard.data['mem_req'],kwargs['runjob_filename'],scard.data['project'])
  return strn
