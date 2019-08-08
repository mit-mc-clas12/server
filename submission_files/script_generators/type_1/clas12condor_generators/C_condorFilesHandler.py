# Handles the file moves and transfer
#
# Notice: hardcoding the name and path: CLAS12_OCRDB.db until DB_path is handled properly
# (Assuming it's in the same dir as where condor submit is executed)
#
# Some relevant quantities:

# $(Process) or $(ProcId)
# Within a cluster of jobs, each takes on its own unique $(Process) or $(ProcId) value.
# The first job has value 0. $(Process) or $(ProcId) will have the same value as the job ClassAd attribute ProcId.
#
# queue 3 in (A, B)
# $(Process) takes on the six values 0, 1, 2, 3, 4, and 5.
# Because there is no specification for the <varname> within this queue command, variable $(Item) is defined.
# It has the value A for the first three jobs queued, and it has the value B for the second three jobs queued.
# $(Step) takes on the three values 0, 1, and 2 for the three jobs with $(Item)=A, and it takes on the same three values 0, 1, and 2 for the three jobs with $(Item)=B.
# $(ItemIndex) is 0 for all three jobs with $(Item)=A, and it is 1 for all three jobs with $(Item)=B.
# $(Row) has the same value as $(ItemIndex) for this example.

def C_condorFilesHandler(scard,**kwargs):

  farm_name = scard.data.get('farm_name')

  # handling mysql or sqlite
  if kwargs['using_sqlite']:
    transfer_input_files = "../utils/database/CLAS12_OCRDB.db"
  else:
    transfer_input_files = "msql_conn.txt"

  # remaining files
  transfer_input_files = transfer_input_files + ", run.sh, nodeScript.sh, job.gcard"


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

# Output directory is defined by the subjob if (or Process)
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
Arguments = {1} $(Process)
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
