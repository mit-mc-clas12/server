# Simulation Details
#
# Memory and CPU
# Executable and Arguments
# Location of Output

def condorJobDetails(scard,**kwargs):
  strn = """
# Hardware requirements
request_cpus   = {0}
request_memory = {1} GB

# script to be executed on the node, and its arguments
Executable = run.sh
Arguments  = {2}

# Error and Output are the error and output channels from your job
# Log is job"s status, success, and resource consumption.
Error  = log/job.$(Cluster).$(Process).err
Output = log/job.$(Cluster).$(Process).out
Log    = log/job.$(Cluster).$(Process).log

# CLAS12 project
+ProjectName = "{3}"
""".format(scard.data['cores_req'],scard.data['mem_req'],kwargs['GcardID'],scard.data['project'])
  
  return strn
