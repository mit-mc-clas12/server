"""

This file, currently under construction, does most of the work
involved in the submission process.  Here is an overview.

1) Retrieve the gcard, username, and scard for this UserSubmissionID
2) Determine the scard type and validate it against fs.valid_scard_types.
3) Build a list of script generators dynamically from the directory
   structure of the project.
4) Get all gcards from online, save locally, and if they're local
   container cards, make sure they exist.
5) Set file extension and database path
6) Call all script builders to write them (script_factory.py)
7) Update FarmSubmissions.run_status field
8) do submission (farm_submission_manager.py)

"""

from __future__ import print_function

# python standard library 
import logging 
import os
import sqlite3
import subprocess
import sys
import time

from importlib import import_module
from subprocess import PIPE, Popen

# local libraries 
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))
                + '/../../utils')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))
                + '/../submission_files/script_generators')
import database
import farm_submission_manager
import fs
import get_args
import lund_helper
import scard_helper
import script_factory
import type_manager
import update_tables
import utils


def process_jobs(args, UserSubmissionID, db_conn, sql):
  """ Submit the job for UserSubmissionID. 

  Detail described in the header of this file.
  I'll write a more useful comment here once the function 
  has been refactored. 

  Inputs: 
  -------
  args - command line arguments 
  UserSubmissionID - (int) from UserSubmissions.UserSubmissionID 
  that drives the submission. 
  db_conn - Active database connection.
  sql - Cursor object for database. 

  """
  logger = logging.getLogger('SubMit')

  fs.DEBUG = getattr(args, fs.debug_long)

  # Grabs UserSubmission and gcards as described in respective files
  username = database.get_username_for_submission(UserSubmissionID, sql)
  user_id = database.get_user_id(username, sql)
  scard = scard_helper.scard_class(database.get_scard_text_for_submission(
    UserSubmissionID, sql))
  logging.debug('For UserSubmissionID = {}, user is {}'.format(
    UserSubmissionID, username))

  scard_type = type_manager.manage_type(args, scard)
  sub_type = 'type_{}'.format(scard_type)
  print("sub_type is {0}".format(sub_type))
  logger.debug('Type manager has determined type is: {}'.format(
    sub_type))

  # Determine the number of jobs this submission
  # will produce in total. 
  njobs = 1 
  if scard_type == 1:
    njobs = int(scard.data['jobs'])
  elif scard_type == 2:
    njobs = lund_helper.count_files(scard.data['generator'])

  # Dynamically load the script generation functions 
  # from the type{sub_type} folder. 
  script_set, script_set_funcs = load_script_generators(sub_type)

  # Setup for different scard types the proper generation options.
  # If external lund files are provided, we go get them.
  set_scard_generator_options(scard, scard_type)

  if scard.data['gcards'] in fs.container_gcards:
    gcard_loc = scard.data['gcards']
  else:
    print('No support for types 3/4 at the present time.')
    exit()

  file_extension = "_UserSubmission_{0}".format(UserSubmissionID)
  
  if fs.use_mysql:
    DB_path = fs.MySQL_DB_path
  else:
    DB_path = fs.SQLite_DB_path

  params = {'table': 'Scards','UserSubmissionID': UserSubmissionID,
            'database_filename': DB_path + fs.DB_name,
            'username': username,'gcard_loc': gcard_loc,
            'file_extension': file_extension,'scard': scard}

  # This is where we actually pass all arguements to write the scripts
  for index, script in enumerate(script_set):
    script_factory.script_factory(args, script, script_set_funcs[index], 
                                  params, db_conn, sql)

  # Update entries in database
  submission_string = 'Submission scripts generated'
  update_tables.update_run_status(submission_string, UserSubmissionID,
                                    db_conn, sql)

  if args.submit:
    print("Submitting jobs to {0} \n".format(scard.data['farm_name']))
    farm_submission_manager.farm_submission_manager(args, UserSubmissionID, 
                                                    file_extension, scard, params, 
                                                    db_conn, sql)
    submission_string = 'Submitted to {0}'.format(scard.data['farm_name'])
    update_tables.update_run_status(submission_string, UserSubmissionID, 
                                    db_conn, sql)

# Move to script factory
def load_script_generators(sub_type):
  """ Dynamically load script generation modules 
  from the directory structure.  """

  logger = logging.getLogger('SubMit')

  # Creating an array of script generating functions.
  script_set = [fs.runscript_file_obj, fs.condor_file_obj, fs.run_job_obj]
  funcs_rs, funcs_condor, funcs_runjob = [], [], [] # initialize empty function arrays
  script_set_funcs = [funcs_rs, funcs_condor, funcs_runjob]

  # Please note, the ordering of this array must match the ordering of the above
  scripts = ["/runscript_generators/","/clas12condor_generators/","/run_job_generators/"]

  # Now we will loop through directories to import the script generation functions
  logger.debug('Scripts = {}'.format(scripts))
  for index, script_dir in enumerate(scripts):
    top_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.abspath(top_dir + '/../submission_files/script_generators/'
                                  + sub_type + script_dir)
    logger.debug('Working with script path: {}'.format(script_path))

    for function in sorted(os.listdir(script_path)):
      if "init" not in function:
        if ".pyc" not in function:
          module_name = function[:-3]
          module = import_module(sub_type + '.' + script_dir[1:-1] + '.' + module_name, 
                                 module_name)
          func = getattr(module, module_name)
          script_set_funcs[index].append(func)
          logger.debug('Importing {}, long name {}'.format(func.__name__, function))
          
  return script_set, script_set_funcs

def set_scard_generator_options(scard, scard_type):
  """ Setup generator options for different types of 
  submissions. 

  Inputs: 
  -------
  - scard - (scard_class) The scard. 
  - scard_type - (int) integer scard type 

  Returns: 
  --------
  - nothing, the scard data is modified inplace. 

  """
  if scard_type in [1,3]:
    scard.data['genExecutable'] = fs.genExecutable.get(scard.data.get('generator'))
    scard.data['genOutput'] = fs.genOutput.get(scard.data.get('generator'))

  elif scard_type in [2,4]:
    scard.data['genExecutable'] = "Null"
    scard.data['genOutput'] = "Null"

def write_gcard(UserSubmissionID):
  """ Write the gcard and return the location.  This 
  will likely be removed in favor of downloading the 
  gcard before job submission (like lund files). """

  utils.printer('Writing gcard to local file')
  newfile = "UserSubmission_{}.gcard".format(UserSubmissionID)
  gfile = fs.sub_files_path + fs.gcards_dir + newfile

  if not os.path.exists(gfile):
    newdir = fs.sub_files_path + fs.gcards_dir

    Popen(['mkdir','-p', newdir], stdout=PIPE)
    Popen(['touch', gfile], stdout=PIPE)

    # Write it out for later. 
    with open(gfile,"w") as output_gcard_file: 
      output_gcard_file.write(gcard_content)

    gcard_loc = 'submission_files/gcards/' + newfile
    return gcard_loc 
