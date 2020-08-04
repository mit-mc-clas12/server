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
    njobs = int(scard.jobs)
  elif scard_type == 2:
    njobs = lund_helper.count_files(scard.generator)

  # Dynamically load the script generation functions
  # from the type{sub_type} folder.
  script_set, script_set_funcs = script_factory.load_script_generators(sub_type)

  # Setup for different scard types the proper generation options.
  # If external lund files are provided, we go get them.
  set_scard_generator_options(scard, scard_type)

  gcard_loc = scard.configuration

  file_extension = "_UserSubmission_{0}".format(UserSubmissionID)

  if fs.use_mysql:
    DB_path = fs.MySQL_DB_path
  else:
    DB_path = fs.SQLite_DB_path

  params = {'table': 'Scards','UserSubmissionID': UserSubmissionID,
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

  print("Submitting jobs to {0} \n".format("OSG")) #Hardcoded for this moment as we removed farm_name from scard
  farm_submission_manager.farm_submission_manager(args, UserSubmissionID,
                                                  file_extension, scard, params,
                                                  db_conn, sql)
  submission_string = 'Submitted to {0}'.format(scard.farm_name)
  update_tables.update_run_status(submission_string, UserSubmissionID,
                                  db_conn, sql)


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
    scard.genExecutable = fs.genExecutable.get(scard.generator)
    scard.genOutput = fs.genOutput.get(scard.generator)

  elif scard_type in [2,4]:
    scard.genExecutable= "Null"
    scard.genOutput = "Null"
