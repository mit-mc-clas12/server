# Handles the files move and transfer
# Notice: hardcoding the name and path: CLAS12_OCRDB.db until DB_path is handled properly
#
# Some relevant quantities:
#
# $(Process) or $(ProcId)
# Within a cluster of jobs, each takes on its own unique $(Process) or $(ProcId) value.
# The first job has value 0. $(Process) or $(ProcId) will have the same value as the job ClassAd attribute ProcId.
#
# queue 3 in (A, B)
# $(Process) takes on the six values 0, 1, 2, 3, 4, and 5.
# Because there is no specification for the <varname> within this queue command, variable $(Item) is defined.
# It has the value A for the first three jobs queued, and it has the value B for the second three jobs queued.
# $(Step) takes on the three values 0, 1, and 2 for the three jobs with $(Item)=A, and it takes on the same
# three values 0, 1, and 2 for the three jobs with $(Item)=B.
#
# $(ItemIndex) is 0 for all three jobs with $(Item)=A, and it is 1 for all three jobs with $(Item)=B.
# $(Row) has the same value as $(ItemIndex) for this example.
#
# A new entry max_idle is used to control how many jobs HTCondor will maintain IDLE.
# For example, if one submits 5000 jobs, 1500 will immediately go to IDLE. As soon as some will run,
# The remaining 3500 will materialize to IDLE then run

def C_condorFilesHandler(scard,**kwargs):

  farm_name = scard.farm_name
  transfer_input_files = ""

  # handling mysql or sqlite
  if kwargs['using_sqlite']:
    transfer_input_files = transfer_input_files + "../utils/database/CLAS12_OCRDB.db, "

  # remaining files
  transfer_input_files = transfer_input_files + "run.sh, nodeScript.sh"

  # MIT Farm: condor wrapper is needed. Notice, path is needed? Can we assume this
  if farm_name == 'MIT_Tier2':
    transfer_input_files = transfer_input_files + ", " + "condor_wrapper"

  strnIO = """
# Input files
transfer_input_files={0}

# How to handle output
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
""".format(transfer_input_files)

  # Output directory is defined by the subjob id (or Process). In this case the farmSubmissionID (same as GcardID)
  strOUTPUT = """
# Output directory is defined by the subjob id (or Process)
transfer_output_files = output
"""

# Arguments to executable: number of jobs and GcardID (same as FarmSubmissionID).
# QUEUE command is the number of jobs
  arguQueue = """
# Arguments given to the executables:
# 1. submission id
# 2. subjob id
#
# Queue starts "jobs" number of subjobs
# max_idle=2000
Arguments = {1} $(Process)
Queue {0}
""".format(scard.jobs, kwargs['user_submission_id'])


  return strnIO + strOUTPUT + arguQueue
