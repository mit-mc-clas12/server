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
import utils, fs, scard_helper, lund_helper, get_args
from script_generators.runscript_generators import runScriptHeader, runGenerator, runGemc, runEvio2hipo, runCooking, runScriptFooter
from script_generators.clas12condor_generators import condorHeader, condorJobDetails, condorFilesHandler
from script_generators.run_job_generators import run_job1

def Submit_batch(args):
  # For debugging, we have a -b --BatchID flag that, if used (i.e. -b 15) will submit that batch only
  # Also, if that batch has already been marked as submitted, it will be passed through again, anyways.

  #First, if the -b flag is used (so batchID is NOT equal to none), we have to make sure that the given
  #batchID actually exists in the database.
  if args.BatchID != 'none':
    Batches = []
    strn = "SELECT BatchID FROM Batches;" #Select all batchIDs from the DB
    Batches_array = utils.db_grab(strn)
    for i in Batches_array: Batches.append(i[0]) #Create a list of all batchIDs
    if not int(args.BatchID) in Batches:   #If the given batchID specified does not exist, throw an error
      print("The selected batch (BatchID = {0}) does not exist, exiting".format(args.BatchID))
      exit()
    else: #If we can find the batchID in the database (i.e. the batchID is valid) pass it to process_jobs()
      BatchID = args.BatchID
      submission_script_manager.process_jobs(args,BatchID)

  #Now we handle the case where a batchID is not specified. This will be normal running operation.
  #Here we will select all batchIDs corresponding to batches that have not yet been simulated, and push
  #Then through the simulation.
  else:
    """
    # There are three options for values in the run_status field in the Submissions table:
    # "Not Submitted", "Submission scripts generated" ,and "Submitted to __",
    # Consider the following cases:
    # 1.) When a user submits a job on the client side, the newly created entry has value "Not Sumbitted"
    # 2.) If the server side code runs without the -s flag, submission scripts will be generated in the DB,
    #     but the jobs will NOT be pushed to HTCondor/Slurm,
    #     and the run_status value will be updated to "Submission scripts generated"
    # 3.) If the server side code runs with the -s flag, ALL jobs that do NOT have the value "Submitted to __"
    #     will have submission scripts generated, and the jobs will be passed to HTCondor/Slurm,
    #     and the value of run_status for all submitted batches will update to "Submitted to __"
    # Case (2) will just create submission scripts for batches created in status (1)
    # Case (3) will create submission scripts and submit jobs for all batches in status (1) and (2)
    """
    if args.submit: #Here, we will grab ALL batches that have NOT been simulated
      strn = "SELECT BatchID FROM Submissions WHERE run_status NOT LIKE '{0}';".format("Submitted to%")
      batches_to_submit = utils.db_grab(strn)
      if len(batches_to_submit) == 0:
        print("There are no batches which have not yet been submitted to a farm")
    else: #Here,if the -s flag was not used, we will just generate submission scripts from batches that have not had any generated yet
      strn = "SELECT BatchID FROM Submissions WHERE run_status = '{0}';".format("Not Submitted")
      batches_to_submit = utils.db_grab(strn)
      if len(batches_to_submit) == 0:
        print("There are no batches which do not yet have submission scripts generated")

   #From the above we have our (non-empty) batch of jobs to submit. Now we can pass it through process_jobs
    if len(batches_to_submit) != 0: #This conditional can probably be removed as it is handled in the above cases
      for Batch in batches_to_submit:
        BatchID = Batch[0] #BatchID is the first element of the tuple
        utils.printer("Generating scripts for batch with BatchID = {0}".format(str(BatchID)))
        submission_script_manager.process_jobs(args,BatchID)


if __name__ == "__main__":
  args = get_args.get_args()
  Submit_batch(args)
