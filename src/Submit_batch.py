#!/usr/bin/env python
#****************************************************************
"""
# This is a sript which executes all scripts needed to generate
submission files from an scard. It just invokes submission_script_maker, and
passes arguements to it.
"""
#****************************************************************

from __future__ import print_function
import argparse, os, sqlite3, subprocess, sys, time
#from subprocess import PIPE, Popen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../utils')
#Could also do the following, but then python has to search the
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import submission_script_maker, htcondor_submit
import file_struct, utils


#This allows a user to specifiy which batch to use to generate files using a specific BatchID
argparser = argparse.ArgumentParser()
argparser.add_argument('-b','--BatchID', default='none', help = 'Enter the ID# of the batch you want to submit (e.g. -b 23)')
argparser.add_argument('-t','--test', help = 'Use this flag (no arguments) if you are NOT on a farm node and want to test the submission flag (-s)', action = 'store_true')
argparser.add_argument('-s','--submit', help = 'Use this flag (no arguments) if you want to submit the job', action = 'store_true')
argparser.add_argument('-w','--write_files', help = 'Use this flag (no arguments) if you want submission files to be written out to text files', action = 'store_true')
argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash, default = file_struct.debug_default,help = file_struct.debug_help)
argparser.add_argument('-l','--lite',help = "use -l or --lite to connect to sqlite DB, otherwise use mysql DB", action = 'store_true')
args = argparser.parse_args()

file_struct.use_mysql = not args.lite
file_struct.DEBUG = getattr(args,file_struct.debug_long)

print("\nGenerating submission files from database")
submission_script_maker.process_jobs(args)
