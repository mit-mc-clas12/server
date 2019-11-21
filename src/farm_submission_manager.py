"""

This module provides functions to distribute
jobs to htcondor.

"""

from __future__ import print_function

import argparse
import os
import sqlite3
import sys
import time
from subprocess import PIPE, Popen

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))
                + '/../../utils')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))
                + '/../submission_files')
import htcondor_submit
import slurm_submit
import update_tables
import utils


def update_users_statistics(scard, params, db_conn, sql):
  strn = "SELECT Total_UserSubmissions FROM Users WHERE User = '{0}';".format(params['username'])
  UserSubmissions_total = utils.db_grab(strn)[0][0]
  UserSubmissions_total += 1
  strn = "UPDATE Users SET Total_UserSubmissions = '{0}' WHERE User = '{1}';".format(UserSubmissions_total,params['username'])
  utils.db_write(strn)
  
  if 'nevents' in scard.data:
    strn = "SELECT Total_Events FROM Users WHERE User = '{0}';".format(params['username'])
    events_total = utils.db_grab(strn)[0][0]
    events_total += int(scard.data['jobs'])*int(scard.data['nevents'])
    strn = "UPDATE Users SET Total_Events = '{0}' WHERE User = '{1}';".format(events_total,params['username'])
    utils.db_write(strn)

  strn = "UPDATE Users SET Most_Recent_Active_Date = '{0}' WHERE User = '{1}';".format(utils.gettime(),params['username'])
  utils.db_write(strn)

def farm_submission_manager(args, GcardID, file_extension,
                            scard, params, db_conn, sql):

  timestamp = utils.gettime() 
  if scard.data['farm_name'] == "MIT_Tier2" or scard.data['farm_name'] == "OSG":
    utils.printer("Passing to htcondor_submit")
    htcondor_submit.htcondor_submit(args,scard,GcardID,file_extension,params)
    update_tables.update_users_statistics(scard, params, timestamp, db_conn, sql)

  elif scard.data['farm_name'] == "JLab":
    utils.printer("Passing to slurm_submit")
    slurm_submit.slurm_submit(args,scard,GcardID,file_extension,params)
    update_tables.update_users_statistics(scard, params, timestamp, db_conn, sql)

  else:
    raise ValueError('Unable to submit for {}'.format(
      scard.data['farm_name']
    ))
