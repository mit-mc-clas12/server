#****************************************************************
"""
# Commentary for this file does not yet exist
"""
#****************************************************************

def run_job1(scard,**kwargs):
  strn = """#!/bin/bash

echo "XXX"
echo "XXX"
pwd;
echo "XXX"
echo "XXX"
ls -l;


echo "-------------"
echo "-------------"
cat condor_wrapper
echo "-------------"
echo "-------------"
cat condor_exec.exe
echo "-------------"
echo "-------------"
cat runscript{0}.sh
echo "-------------"
echo "-------------"

./condor_wrapper /tmp/runscript{0}.sh""".format(kwargs['file_extension'])
  return strn
