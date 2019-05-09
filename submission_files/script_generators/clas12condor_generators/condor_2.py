#****************************************************************
"""
# Commentary for this file does not yet exist
"""
#****************************************************************

def condor_2(scard,**kwargs):
  strn = """#Input files. Do not add comments after the file list
  # transfer_input_files = cook.csh

  # output
  should_transfer_files = YES
  when_to_transfer_output = ON_EXIT
  transfer_input_files={0}, condor_wrapper
  transfer_output_files = out_$(Cluster)_n{1}

  # QUEUE is the "start button" - it launches any jobs that have been
  # specified thus far. 1 means launch only 1 job
  Queue {2}\n""".format(kwargs['runscript_filename'],scard.data['nevents'],scard.data['jobs'])
  return strn
