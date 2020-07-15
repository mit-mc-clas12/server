"""

This module provides functions that
dynamically load the scripts from a
directory or directry tree.

It's used in the importation of type
scripts (submission_script_manager.py).

"""

from __future__ import print_function
import logging
import os
import sqlite3
import subprocess
import sys
import time
from importlib import import_module

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../utils')
import farm_submission_manager
import fs
import get_args
import lund_helper
import scard_helper
import update_tables
import utils

# Generates a script by appending functions that output strings
# This function is called by submission_script_manager.py
def script_factory(args, script_obj, script_functions, params, db_conn, sql):

  logger = logging.getLogger('SubMit')

  runscript_filename = fs.runscript_file_obj.file_path + \
                       fs.runscript_file_obj.file_base
  runscript_filename += params['file_extension'] + \
                        fs.runscript_file_obj.file_end
  #runjob_filename = fs.run_job_obj.file_path + fs.run_job_obj.file_base
  #runjob_filename = runjob_filename + params['file_extension'] + \
  #                  fs.run_job_obj.file_end

  # In the below for loop, we loop through all script_generators
  # for a certain submission script, appending the output of each
  # function to a string

  gen_text = [f(params['scard'],
                username=params['username'],
                gcard_loc=params['gcard_loc'],
                user_submission_id=params['UserSubmissionID'],
                file_extension=params['file_extension'],
                runscript_filename=runscript_filename,
                #runjob_filename=runjob_filename,
                using_sqlite=args.lite,) for f in script_functions]

  script_text = "".join(gen_text)

  # Write files to a local directory
  if args.write_files:
    filename = os.path.normpath(script_obj.file_path
                                + script_obj.file_base
                                + params['file_extension']
                                + script_obj.file_end)

    logger.debug(("\tWriting submission file '{0}' based off of specs "
                  "of UserSubmissionID = {1}").format(
                    filename, params['UserSubmissionID']))

    if not os.path.exists(os.path.normpath(script_obj.file_path)):
      logger.debug('Creating directory: {}'.format(script_obj.file_path))
      subprocess.call(['mkdir','-p',script_obj.file_path],
                      stdout=subprocess.PIPE)

    if os.path.isfile(filename):
      subprocess.call(['rm',filename])

    subprocess.call(['touch', filename])
    with open(filename, 'w') as f:
      f.write(script_text)

  # Write out to the database, regardless of the value of args.write_files.
  #
  # I can't figure out a way to write "" into a sqlite field without errors
  # For now, we can replace " with ', which works ok,
  # but IDK how it will run if the scripts were submitted to HTCondor
  str_script_db = script_text.replace('"',"'")
  update_tables.update_run_script(
    script_obj.file_text_fieldname, str_script_db, params['UserSubmissionID'],
    db_conn, sql
  )

def load_script_generators(sub_type):
  """ Dynamically load script generation modules
  from the directory structure.  """

  logger = logging.getLogger('SubMit')

  # Creating an array of script generating functions.
  script_set = [fs.runscript_file_obj, fs.condor_file_obj]
#  script_set = [fs.runscript_file_obj, fs.condor_file_obj, fs.run_job_obj]
  funcs_rs, funcs_condor, funcs_runjob = [], [], [] # initialize empty function arrays
  script_set_funcs = [funcs_rs, funcs_condor, funcs_runjob]

  # Please note, the ordering of this array must match the ordering of the above
  scripts = ["/runscript_generators/","/clas12condor_generators/"]
#  scripts = ["/runscript_generators/","/clas12condor_generators/","/run_job_generators/"]

  # Now we will loop through directories to import the script generation functions
  logger.debug('Scripts = {}'.format(scripts))
  for index, script_dir in enumerate(scripts):
    top_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.abspath(top_dir + '/../submission_files/script_generators/'
                                  + sub_type + script_dir)
    logger.debug('Working with script path: {}'.format(script_path))

    for function in sorted(os.listdir(script_path)):
      if "init" not in function:
          if "__pycache__" not in function:
            if ".pyc" not in function:
              module_name = function[:-3]
              module = import_module(sub_type + '.' + script_dir[1:-1] + '.' + module_name,
                                     module_name)
              func = getattr(module, module_name)
              script_set_funcs[index].append(func)
              logger.debug('Importing {}, long name {}'.format(func.__name__, function))

  return script_set, script_set_funcs
