#****************************************************************
"""
# This distribuits job sumbissions to HTCondor, SLURM, etc. based off what the node runs.
"""
#****************************************************************

from __future__ import print_function
import argparse, os, sqlite3, subprocess, sys, time
from subprocess import PIPE, Popen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../utils')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../submission_files')
#Could also do the following, but then python has to search the
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import htcondor_submit, slurm_submit
import submission_script_maker
import file_struct, utils

"""The below can be extended in a better way for more farms, e.g. create a dictionary"""
def farm_submission_manager(args,GcardID,file_extension,scard):
  if scard.data['farm_name'] == "MIT_Tier2" or scard.data['farm_name'] == "OSG":
    utils.printer("Passing to htcondor_submit")
    htcondor_submit.htcondor_submit(args,GcardID,file_extension)
  elif scard.data['farm_name'] == "JLab":
    utils.printer("Passing to slurm_submit")
    slurm_submit.slurm_submit(args,GcardID,file_extension)
  else:
    print('Invalid farm name in scard, please check that the desired farm is spelled correctly and is supported')
    exit()
