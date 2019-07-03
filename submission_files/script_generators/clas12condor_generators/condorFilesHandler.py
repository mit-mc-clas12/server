# Handles the file moves and transfer
#
# Notice: hardcoding the name and path: CLAS12_OCRDB.db until DB_path is handled properly
# (Assuming it's in the same dir as where condor submit is executed)
#

def condorFilesHandler(scard,**kwargs):

  farm_name = scard.data.get('farm_name')
  # if it's a test, the Database should be copied
  # for now, copying it anyway, but path is hardcoded
  # transfer_input_files={0}, condor_wrapper

  if kwargs['using_sqlite']:
    transfer_input_files = "../utils/database/CLAS12_OCRDB.db"
  else:
    transfer_input_files = "msqlconf.txt"
  if 'http' in scard.data.get('generator'):
    transfer_input_files = transfer_input_files

  # MIT Farm: condor wrapper is needed. Notice, path is needed? Can we assume this
  if farm_name == 'MIT_Tier2':
    transfer_input_files = transfer_input_files + ", " + "condor_wrapper"

  # Input and Outut files
  #######################
  strnIO = """

# Input files
transfer_input_files={0}

# How to handle output
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
""".format(transfer_input_files)

  # Lund submission
  if 'http' in scard.data.get('generator'):
    strnIO = """
# Input files
transfer_input_files={0}, $(lundFile)

# How to handle output
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
""".format(transfer_input_files)


  # Output file is defined based on the submission id (GcardID) and the subjob id (Steo)
  strOUTPUT = """

# Output directory is defined by the subjob if (or Step)
#transfer_output_files = out_{0}/simu_$(Step)
transfer_output_files = out_{0}
""".format(kwargs['GcardID'])

  # Argumnent to executable and QUEUE command.
  ############################################

  # no Lund
  arguQueue = """
# Arguments given to the executables:
# 1. submission id
# 2. subjob id
#
# Queue starts "jobs" number of subjobs
Arguments = {1} $(Step)
Queue {0}
""".format(scard.data['jobs'], kwargs['GcardID'])


  # Lund submission
  if 'http' in scard.data.get('generator'):
    arguQueue = """
# Arguments given to the executables:
# 1. submission id
# 2. subjob id
# 3. lundfile, given by the queue comand
#
# Queue starts "jobs" number of subjobs
Arguments  = {1} $(Process) $(lundFile)
queue lundFile matching files {2}/*.txt
""".format(scard.data['jobs'], kwargs['GcardID'], kwargs['lund_dir'])

  return strnIO + strOUTPUT + arguQueue
