# Handles the file moves and transfer
#
# Notice: hardcoding the name and path: CLAS12_OCRDB.db until DB_path is handled properly
# (Assuming it's in the same dir as where condor submit is executed)
#

def condorFilesHandler(scard,**kwargs):
  strn = """
# Input files
#transfer_input_files={0}, condor_wrapper
transfer_input_files=CLAS12_OCRDB.db, condor_wrapper

# Output directory
transfer_output_files   = out_{2}

# How to handle output
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT

# QUEUE is the "start button" - it launches any jobs that have been
# specified thus far. 1 means launch only 1 job
Queue {1}\n

""".format(kwargs['database_filename'],scard.data['jobs'], kwargs['GcardID'])

  return strn
