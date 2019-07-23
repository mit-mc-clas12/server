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
from subprocess import PIPE, Popen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../utils')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../submission_files/script_generators')
import farm_submission_manager, script_factory
import utils, fs, scard_helper, lund_helper, get_args
from runscript_generators import *
from clas12condor_generators import *
from run_job_generators import *


def process_jobs(args,BatchID):
  fs.DEBUG = getattr(args,fs.debug_long)
  # Grabs batch and gcards as described in respective files
  gcards = utils.db_grab("SELECT GcardID, gcard_text FROM Gcards WHERE BatchID = {0};".format(BatchID))
  username = utils.db_grab("SELECT User FROM Batches WHERE BatchID = {0};".format(BatchID))[0][0]
  scard = scard_helper.scard_class(utils.db_grab( "SELECT scard FROM Batches WHERE BatchID = {0};".format(BatchID))[0][0])

  # script to be run inside the container
  funcs_rs = (runScriptHeader.runScriptHeader,
              runGenerator.runGenerator,
              runGemc.runGemc,
              runEvio2hipo.runEvio2hipo,
              runCooking.runCooking,
              runScriptFooter.runScriptFooter)

  # condor submission script
  funcs_condor = (condorHeader.condorHeader,
                  condorJobDetails.condorJobDetails,
                  condorFilesHandler.condorFilesHandler)

  # condor wrapper
  funcs_runjob = (run_job1.run_job1,)

  if 'http' in scard.data.get('generator'):
    lund_dir = lund_helper.Lund_Entry(scard.data.get('generator'))
    scard.data['genExecutable'] = "Null"
    scard.data['genOutput'] = "Null"
  else:
    lund_dir = 0
    scard.data['genExecutable'] = fs.genExecutable.get(scard.data.get('generator'))
    scard.data['genOutput'] = fs.genOutput.get(scard.data.get('generator'))

  # Now we create job submissions for all jobs that were recognized
  for gcard in gcards:
    GcardID = gcard[0]

    if scard.data['gcards'] == fs.gcard_default:
      gcard_loc = scard.data['gcards']
    elif 'http' in  scard.data['gcards']:
      utils.printer('Writing gcard to local file')
      newfile = "gcard_{0}_batch_{1}.gcard".format(GcardID,BatchID)
      gfile= fs.sub_files_path+fs.gcards_dir+newfile
      if not os.path.exists(gfile):#fs.sub_files_path+fs.gcards_dir):
        newdir = fs.sub_files_path+fs.gcards_dir
        print("newdir is {0}".format(newdir))
        Popen(['mkdir','-p',newdir], stdout=PIPE)
        Popen(['touch',gfile], stdout=PIPE)
      with open(gfile,"w") as file: file.write(gcard[1])
      gcard_loc = 'submission_files/gcards/'+newfile
    else:
      print('gcard not recognized as default option or online repository, please inspect scard')
      exit()

    file_extension = "_gcard_{0}_batch_{1}".format(GcardID,BatchID)

    if fs.use_mysql:
      DB_path = fs.MySQL_DB_path
    else:
      DB_path = fs.SQLite_DB_path

    params = {'table':'Scards','BatchID':BatchID,'GcardID':GcardID,
              'database_filename':DB_path+fs.DB_name,
              'username':username,'gcard_loc':gcard_loc,'lund_dir':lund_dir,
              'file_extension':file_extension,'scard':scard}

    script_set = [fs.runscript_file_obj,fs.condor_file_obj,fs.run_job_obj]
    script_set_funcs = [funcs_rs,funcs_condor,funcs_runjob]

    """ This is where we actually pass all arguements to write the scripts"""
    for index, script in enumerate(script_set):
      script_factory.script_factory(args, script, script_set_funcs[index], params)

    print("\tSuccessfully generated submission files for Batch {0} with GcardID {1}".format(BatchID,GcardID))

    submission_string = 'Submission scripts generated'.format(scard.data['farm_name'])
    strn = "UPDATE Submissions SET {0} = '{1}' WHERE BatchID = {2};".format('run_status',submission_string,BatchID)
    utils.db_write(strn)

    if args.submit:
      print("\tSubmitting jobs to {0} \n".format(scard.data['farm_name']))
      farm_submission_manager.farm_submission_manager(args,GcardID,file_extension,scard,params)
      submission_string = 'Submitted to {0}'.format(scard.data['farm_name'])
      strn = "UPDATE Submissions SET {0} = '{1}' WHERE BatchID = {2};".format('run_status',submission_string,BatchID)
      utils.db_write(strn)
