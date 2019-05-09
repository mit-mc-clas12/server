#****************************************************************
"""
# This is actually submits on a computer pool. Currently configured
# To work on HTCondor, tested on a SubMIT node. Not working perfectly yet
"""
#****************************************************************

from __future__ import print_function
import argparse, os, sqlite3, subprocess, sys, time
from subprocess import PIPE, Popen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../utils')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../submission_files')
#Could also do the following, but then python has to search the
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import submission_script_maker
import file_struct, utils

#This allows a user to specifiy which batch to use to generate files using a specific BatchID
argparser = argparse.ArgumentParser()
argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
argparser.add_argument('-b','--BatchID', default='none', help = 'Enter the ID# of the batch you want to submit (e.g. -b 23)')
argparser.add_argument('-s','--submit', help = 'Use this flag (no arguements) if you want to submit the job', action = 'store_true')
args = argparser.parse_args()

dirname = os.path.dirname(__file__)

if dirname == '': dirname = '.'

def htcondor_submit(args,GcardID,file_extension):

  """ if value in submission === not submitted"""

  runscript_file = file_struct.runscript_file_obj.file_base + file_extension + file_struct.runscript_file_obj.file_end
  clas12condor_file = file_struct.condor_file_obj.file_base + file_extension + file_struct.condor_file_obj.file_end

  condorfile = 'submission_files/'+'condor_files/' + clas12condor_file

  subprocess.call(['chmod','+x',file_struct.runscript_file_obj.file_path + runscript_file])
  subprocess.call(['chmod','+x',"condor_wrapper"])
  submission = Popen(['condor_submit',condorfile], stdout=PIPE).communicate()[0]
  #The below is for testing purposes
  #submission = """Submitting job(s)...
  #3 job(s) submitted to cluster 7334290."""
  print(submission)
  words = submission.split()
  node_number = words[len(words)-1] #This might only work on SubMIT
  print(node_number)

  strn = "UPDATE Submissions SET run_status = 'submitted to pool' WHERE GcardID = '{0}';".format(GcardID)
  utils.sql3_exec(strn)

  timestamp = utils.gettime() # Can modify this if need 10ths of seconds or more resolution
  strn = "UPDATE Submissions SET submission_timestamp = '{0}' WHERE GcardID = '{1}';".format(timestamp,GcardID)
  utils.sql3_exec(strn)

  strn = "UPDATE Submissions SET pool_node = '{0}' WHERE GcardID = '{1}';".format(node_number,GcardID)
  utils.sql3_exec(strn)



if __name__ == "__main__":
  argparser = argparse.ArgumentParser()
  argparser.add_argument('-b','--BatchID', default='none', help = 'Enter the ID# of the batch you want to submit (e.g. -b 23)')
  argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
  argparser.add_argument('-s','--submit', help = 'Use this flag (no arguements) if you want to submit the job', action = 'store_true')
  args = argparser.parse_args()

  file_struct.DEBUG = getattr(args,file_struct.debug_long)

  submission_script_maker(args)
