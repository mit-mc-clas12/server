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

def farm_submission_manager(args, GcardID, file_extension,
                            scard, params, db_conn, sql):

  timestamp = utils.gettime() 
  if scard.data['farm_name'] == "MIT_Tier2" or scard.data['farm_name'] == "OSG":
    utils.printer("Passing to htcondor_submit")
    htcondor_submit.htcondor_submit(args,scard,GcardID,file_extension,params,
                                    db_conn, sql)
    update_tables.update_users_statistics(scard, params, timestamp, db_conn, sql)

  elif scard.data['farm_name'] == "JLab":
    utils.printer("Passing to slurm_submit")
    slurm_submit.slurm_submit(args,scard,GcardID,file_extension,params)
    update_tables.update_users_statistics(scard, params, timestamp, db_conn, sql)

  else:
    raise ValueError('Unable to submit for {}'.format(
      scard.data['farm_name']
    ))
