#****************************************************************
"""
# File Description
"""
#****************************************************************
from __future__ import print_function
import os, sqlite3, subprocess, sys, time
from subprocess import PIPE, Popen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../utils')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../submission_files/script_generators')
import farm_submission_manager, script_factory
import utils, fs, scard_helper, lund_helper, get_args
from importlib import import_module

def manage_type(args,scard):
  print("in type manager")
  custom_gcard_identifier = "http"
  custom_lund_identifier = "http"
  scard_type = 1 #Default value, will be modified only if identifiers are found in scard
  lund_type_mod, gcard_type_mod = 0, 0

  if custom_lund_identifier in scard.data.get('generator'):
    lund_type_mod = 1
  if custom_gcard_identifier in  scard.data['gcards']:
    gcard_type_mod = 2

  #If using default scard,         type = 1
  #If using custom lund,           type = 1 + 1 = 2
  #If using custom gcard,          type = 1 + 2 = 3
  #If using custom lund and gcard, type = 1 + 1 + 2 = 4
  return scard_type + lund_type_mod + gcard_type_mod
