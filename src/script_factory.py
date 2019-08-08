#****************************************************************
"""
# Enter file description here
"""
#****************************************************************
from __future__ import print_function
import os, sqlite3, subprocess, sys, time
from subprocess import PIPE, Popen

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../utils')
import farm_submission_manager
import utils, fs, scard_helper, lund_helper, get_args

#Generates a script by appending functions that output strings
#This function is called by submission_script_manager.py
def script_factory(args,script_obj,script_functions,params):

  script_text = ""
  runscript_filename=fs.runscript_file_obj.file_path+fs.runscript_file_obj.file_base
  runscript_filename= runscript_filename + params['file_extension'] + fs.runscript_file_obj.file_end
  runjob_filename=fs.run_job_obj.file_path+fs.run_job_obj.file_base
  runjob_filename= runjob_filename+ params['file_extension'] + fs.run_job_obj.file_end

  #In the below for loop, we loop through all script_generators for a certain submission script, appending the output of each function to a string
  gen_text = [f(params['scard'],
              username=params['username'],
              gcard_loc=params['gcard_loc'],
              GcardID = params['GcardID'],
              lund_dir = params['lund_dir'],
              database_filename = params['database_filename'],
              file_extension = params['file_extension'],
              runscript_filename=runscript_filename,
              runjob_filename=runjob_filename,
              using_sqlite = args.lite,) for f in script_functions]

  script_text = script_text.join(gen_text)

  #This handles writing to disk and to SQL database
  if args.write_files:
    filename = script_obj.file_path+script_obj.file_base+params['file_extension']+script_obj.file_end
    utils.printer("\tWriting submission file '{0}' based off of specifications of UserSubmissionID = {1}, GcardID = {2}".format(filename,
        params['UserSubmissionID'],params['GcardID']))
    if not os.path.exists(script_obj.file_path):
        Popen(['mkdir','-p',script_obj.file_path], stdout=PIPE)
    if os.path.isfile(filename):
      subprocess.call(['rm',filename])
    Popen(['touch',filename], stdout=PIPE)
    with open(filename,"w") as file: file.write(script_text)
  str_script_db = script_text.replace('"',"'") #I can't figure out a way to write "" into a sqlite field without errors
  # For now, we can replace " with ', which works ok, but IDK how it will run if the scripts were submitted to HTCondor
  strn = 'UPDATE FarmSubmissions SET {0} = "{1}" WHERE GcardID = {2};'.format(script_obj.file_text_fieldname,str_script_db,params['GcardID'])
  utils.db_write(strn)
