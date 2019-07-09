#****************************************************************
"""
# This file will query the command line to see what BatchID it should use,
# or if no arguement is given on the CL, the most recent BatchID will be used
# This BatchID is used to identify the proper scard and gcards, and then submission
# files corresponding to each gcard are generated and stored in the database, as
# well as written out to a file with a unique name. This latter part will be passed
# to the server side in the near future.
"""
#****************************************************************
from __future__ import print_function
import os, sqlite3, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../utils')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../submission_files')
import farm_submission_manager, script_factory, submission_script_manager
import utils, file_struct, scard_helper, lund_helper, get_args
from script_generators.runscript_generators import runScriptHeader, runGenerator, runGemc, runEvio2hipo, runCooking, runScriptFooter
from script_generators.clas12condor_generators import condorHeader, condorJobDetails, condorFilesHandler
from script_generators.run_job_generators import run_job1

def Submit_batch(args):
  if args.BatchID != 'none':
    Batches = []
    strn = "SELECT BatchID FROM Batches;"
    Batches_array = utils.sql3_grab(strn)
    for i in Batches_array: Batches.append(i[0])
    if not int(args.BatchID) in Batches:
      print("The selected batch (BatchID = {0}) does not exist, exiting".format(args.BatchID))
      exit()
    else:
      BatchID = args.BatchID
      submission_script_manager.process_jobs(args,BatchID)
  else:
    if args.submit:
      strn = "SELECT BatchID FROM Submissions WHERE run_status NOT LIKE '{0}';".format("Submitted to%")
      batches_to_submit = utils.sql3_grab(strn)
      if len(batches_to_submit) == 0:
        print("There are no batches which have not yet been submitted to a farm")
    else:
      strn = "SELECT BatchID FROM Submissions WHERE run_status = '{0}';".format("Not Submitted")
      batches_to_submit = utils.sql3_grab(strn)
      if len(batches_to_submit) == 0:
        print("There are no batches which do not yet have submission scripts generated")
    if len(batches_to_submit) != 0:
      for Batch in batches_to_submit:
        BatchID = Batch[0]
        utils.printer("Generating scripts for batch with BatchID = {0}".format(str(BatchID)))
        submission_script_manager.process_jobs(args,BatchID)


if __name__ == "__main__":
  args = get_args.get_args()
  Submit_batch(args)
