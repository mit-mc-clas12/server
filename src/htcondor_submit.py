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

  condorfile = fs.condor_file_obj.file_path + clas12condor_file
  #subprocess.call(['chmod','+x',fs.runscript_file_obj.file_path + runscript_file]) #No longer need to do this
  condorwrapper_location = this_dirname+"/../condor_wrapper"
  subprocess.call(['chmod','+x',condorwrapper_location])

  if args.test:
    output_dir_base = this_dirname+"/volatile/clas12/osg/"
  else:
    output_dir_base = "/volatile/clas12/osg/"
  condor_exec = this_dirname + "/../condor_submit.sh"
  run_mysql_exec = this_dirname + "/../run_mysql.sh"
  run_sqlite_exec = this_dirname + "/../run_sqlite.sh"
  login_info = this_dirname + "/../../msqlr.txt"

  #if args.test:
  #  submission = """THIS IS A FAKE SUBMISSION...
#    3 job(s) submitted to cluster 7334290."""#
#  else:
    #print("trying to submit job with popen")
    #subprocess.call(['cd',scard.data["output_dir"]])
    #submission = Popen(['condor_submit',condorfile], stdout=PIPE).communicate()[0]
  if args.lite:
    login_info = this_dirname + "/../../utils/msql.txt"
    subprocess.call([condor_exec,condorfile,output_dir_base,params['username'],run_sqlite_exec,str(args.test),login_info])
  else:
    print("Fill in mysql conditions here")
    #subprocess.call([condor_exec,params['username'],condorfile,run_sqlite_exec,msql_info])

"""
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
"""
