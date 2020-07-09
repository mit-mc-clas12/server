"""

This module contains a function that
infers the type of scard based on the
content of the fields.

"""

from __future__ import print_function

# python standard lib
import os
import sqlite3
import sys
import time
from importlib import import_module
from subprocess import PIPE, Popen

# this project
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../utils')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../submission_files/script_generators')
import fs


def manage_type(args, scard):
  """

  Type manager is used to infer the scard
  type based on the content.

  Examples:
  ---------
  - If using default scard,         type = 1
  - If using custom lund,           type = 1 + 1 = 2
  - If using custom gcard,          type = 1 + 2 = 3
  - If using custom lund and gcard, type = 1 + 1 + 2 = 4

  Inputs:
  -------
  - args - command line arguments, currently not used
  and should be removed
  - scard - (scard_class) the data of which is used to
  determine the type of scard

  Returns:
  --------
  - scard_type (int)

  """
  custom_gcard_identifier = "http"
  custom_lund_identifier = "http"
  scard_type = 1
  lund_type_mod, gcard_type_mod = 0, 0

  if scard.generator not in fs.genExecutable:
    lund_type_mod = 1
  #if custom_gcard_identifier in scard.configuration:
   # gcard_type_mod = 2

  return (scard_type + lund_type_mod + gcard_type_mod)
