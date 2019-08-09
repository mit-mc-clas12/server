#****************************************************************
"""
# This file will query the command line to see what UserSubmissionID it should use,
# or if no arguement is given on the CL, the most recent UserSubmissionID will be used
# This UserSubmissionID is used to identify the proper scard and gcards, and then submission
# files corresponding to each gcard are generated and stored in the database, as
# well as written out to a file with a unique name. This latter part will be passed
# to the server side in the near future.
"""
#****************************************************************
from __future__ import print_function
import os, sqlite3, subprocess, sys, time
from subprocess import PIPE, Popen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../utils')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../submission_files/script_generators')
import farm_submission_manager, script_factory, type_manager
import utils, fs, scard_helper, lund_helper, get_args
from importlib import import_module

def process_jobs(args,UserSubmissionID):
  fs.DEBUG = getattr(args,fs.debug_long)
  # Grabs UserSubmission and gcards as described in respective files
  gcards = utils.db_grab("SELECT GcardID, gcard_text FROM Gcards WHERE UserSubmissionID = {0};".format(UserSubmissionID))
  username = utils.db_grab("SELECT User FROM UserSubmissions WHERE UserSubmissionID = {0};".format(UserSubmissionID))[0][0]
  scard = scard_helper.scard_class(utils.db_grab( "SELECT scard FROM UserSubmissions WHERE UserSubmissionID = {0};".format(UserSubmissionID))[0][0])

  #This block picks up the scard type from arguements and throws an error if it was not an int
  try:
    scard_type = int(args.scard_type)
  except Exception as err:
    print("There was an error in recognizing scard type: ")
    print(err)
    exit()

  #Setting sub_type to the right directory based on the scard_type

  if scard_type in fs.valid_scard_types:
    sub_type = "type_{0}".format(scard_type)
    print("Using scard type {0} template".format(scard_type))
  elif scard_type == 0:
    sub_type = "type_{0}".format(type_manager.manage_type(args,scard))
  else:
    print("Poorly defined scard_type: {0}. Below is a list of valid scard types. Exiting".format(scard_type))
    for type in fs.valid_scard_types:
      print("Valid scard type: {0}".format(type))
    exit()

  print("sub_type is {0}".format(sub_type))

  #This is creating an array of script generating functions.
  script_set = [fs.runscript_file_obj,fs.condor_file_obj,fs.run_job_obj]
  funcs_rs, funcs_condor,funcs_runjob = [], [], [] #initialize empty function arrays
  script_set_funcs = [funcs_rs,funcs_condor,funcs_runjob]
  #Please note, the ordering of this array must match the ordering of the above
  scripts = ["/runscript_generators/","/clas12condor_generators/","/run_job_generators/"]

  #Now we will loop through directories to import the script generation functions
  for index, script_dir in enumerate(scripts):
    for function in os.listdir("submission_files/script_generators/"+sub_type+script_dir):
      if "init" not in function:
        if ".pyc" not in function:
          module_name = function[:-3]
          module = import_module(sub_type+'.'+script_dir[1:-1]+'.'+module_name,module_name)
          func = getattr(module,module_name)
          script_set_funcs[index].append(func)

  if 'http' in scard.data.get('generator'):
    lund_dir = lund_helper.Lund_Entry(scard.data.get('generator'))
    scard.data['genExecutable'] = "Null"
    scard.data['genOutput'] = "Null"
  else:
    lund_dir = 0
    scard.data['genExecutable'] = fs.genExecutable.get(scard.data.get('generator'))
    scard.data['genOutput'] = fs.genOutput.get(scard.data.get('generator'))

  # Now we create job submissions for all jobs that were recognized
  for gcard in gcards:
    GcardID = gcard[0]

    if scard.data['gcards'] == fs.gcard_default:
      gcard_loc = scard.data['gcards']
    elif 'http' in  scard.data['gcards']:
      utils.printer('Writing gcard to local file')
      newfile = "gcard_{0}_UserSubmission_{1}.gcard".format(GcardID,UserSubmissionID)
      gfile= fs.sub_files_path+fs.gcards_dir+newfile
      if not os.path.exists(gfile):
        newdir = fs.sub_files_path+fs.gcards_dir
        print("newdir is {0}".format(newdir))
        Popen(['mkdir','-p',newdir], stdout=PIPE)
        Popen(['touch',gfile], stdout=PIPE)
      with open(gfile,"w") as file: file.write(gcard[1])
      gcard_loc = 'submission_files/gcards/'+newfile
    else:
      print('gcard not recognized as default option or online repository, please inspect scard')
      exit()

    file_extension = "_gcard_{0}_UserSubmission_{1}".format(GcardID,UserSubmissionID)

    if fs.use_mysql:
      DB_path = fs.MySQL_DB_path
    else:
      DB_path = fs.SQLite_DB_path

    params = {'table':'Scards','UserSubmissionID':UserSubmissionID,'GcardID':GcardID,
              'database_filename':DB_path+fs.DB_name,
              'username':username,'gcard_loc':gcard_loc,'lund_dir':lund_dir,
              'file_extension':file_extension,'scard':scard}


    """ This is where we actually pass all arguements to write the scripts"""
    for index, script in enumerate(script_set):
      script_factory.script_factory(args, script, script_set_funcs[index], params)

    print("\tSuccessfully generated submission files for UserSubmission {0} with GcardID {1}".format(UserSubmissionID,GcardID))

    submission_string = 'Submission scripts generated'.format(scard.data['farm_name'])
    strn = "UPDATE FarmSubmissions SET {0} = '{1}' WHERE UserSubmissionID = {2};".format('run_status',submission_string,UserSubmissionID)
    utils.db_write(strn)

    if args.submit:
      print("\tSubmitting jobs to {0} \n".format(scard.data['farm_name']))
      farm_submission_manager.farm_submission_manager(args,GcardID,file_extension,scard,params)
      submission_string = 'Submitted to {0}'.format(scard.data['farm_name'])
      strn = "UPDATE FarmSubmissions SET {0} = '{1}' WHERE UserSubmissionID = {2};".format('run_status',submission_string,UserSubmissionID)
      utils.db_write(strn)
