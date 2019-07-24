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
  this_dirname = os.path.dirname(os.path.abspath(__file__))#os.path.dirname(__file__)

  runscript_file = fs.runscript_file_obj.file_base + file_extension + fs.runscript_file_obj.file_end
  clas12condor_file = fs.condor_file_obj.file_base + file_extension + fs.condor_file_obj.file_end

  condorfile_loc = fs.condor_file_obj.file_path + clas12condor_file
  #subprocess.call(['chmod','+x',fs.runscript_file_obj.file_path + runscript_file]) #No longer need to do this
  condorwrapper_location = this_dirname+"/../condor_wrapper"
  subprocess.call(['chmod','+x',condorwrapper_location])

  if args.OutputDir != 'none':
    print("Using custom directory for output at {0}".format(args.OutputDir))
    output_dir_base = args.OutputDir
  else:
    if args.test:
      output_dir_base = this_dirname+"/volatile/clas12/osg"
    else:
      output_dir_base = "/volatile/clas12/osg"

  condor_exec = this_dirname + "/../condor_submit.sh"
  run_mysql_exec = this_dirname + "/../run_mysql.sh"
  run_sqlite_exec = this_dirname + "/../run_sqlite.sh"

  if args.lite:
    print("Since you used the -t flag, the command 'condor_submit clas12.condor will not be passed'")
    submission = Popen([condor_exec,condorfile_loc,clas12condor_file,output_dir_base,
      params['username'],run_sqlite_exec,str(args.test)], stdout=PIPE).communicate()[0]
  else:
    print("Trying to execute condor_submit.sh now")
    submission = Popen([condor_exec,condorfile_loc,clas12condor_file,output_dir_base,
      params['username'],run_mysql_exec,str(args.test)], stdout=PIPE).communicate()[0]

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
