#****************************************************************
"""
# This is actually submits a job on a computer pool running SLURM
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


def slurm_submit(args,scard,GcardID,file_extension,params):

  """ THIS CODE NEEDS TO BE CREATED """

  print(""" CODE FOR SLURM DOES NOT YET EXIST, PLEASE WRITE """)

  exit()
