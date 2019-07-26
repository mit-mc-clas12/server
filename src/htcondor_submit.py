#****************************************************************
"""
# This is actually submits a job on a computer pool running HTCondor
"""
#****************************************************************

from __future__ import print_function
import argparse, os, sqlite3, subprocess, sys, time
from subprocess import PIPE, Popen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../utils')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../submission_files')
#Could also do the following, but then python has to search the
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import Submit_UserSubmission
import fs, utils

def htcondor_submit(args,scard,GcardID,file_extension,params):

  """ if value in submission === not submitted"""
  # Need to add condition here in case path is different for non-jlab
  scripts_baseDir  = "/group/clas12/SubMit"
  condor_exec = scripts_baseDir + "/server/condor_submit.sh"
  jobOutputDir = "/volatile/clas12/osg"


  # don't know how to pass farmsubmissionID (4th argument), passing GcardID for now (it may be the same)
  submission = Popen([condor_exec, scripts_baseDir, jobOutputDir, params['username'], str(GcardID)], stdout=PIPE).communicate()[0]

  print(submission)

  words = submission.split()
  node_number = words[len(words)-1] #This might only work on SubMIT

  strn = "UPDATE FarmSubmissions SET run_status = 'submitted to pool' WHERE GcardID = '{0}';".format(GcardID)
  utils.db_write(strn)

  timestamp = utils.gettime() # Can modify this if need 10ths of seconds or more resolution
  strn = "UPDATE FarmSubmissions SET submission_timestamp = '{0}' WHERE GcardID = '{1}';".format(timestamp,GcardID)
  utils.db_write(strn)

  strn = "UPDATE FarmSubmissions SET pool_node = '{0}' WHERE GcardID = '{1}';".format(node_number,GcardID)
  utils.db_write(strn)
