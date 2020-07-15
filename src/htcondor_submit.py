"""

Submit a job using htcondor.

"""

from __future__ import print_function

import os
import sys
from subprocess import PIPE, Popen

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../utils')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../submission_files')
import fs
import utils
import update_tables

def htcondor_submit(args, scard, usub_id, file_extension, params, db_conn, sql):


    jobOutputDir = args.OutputDir

    if args.test_condorscript:
        scripts_baseDir  = os.path.dirname(os.path.abspath(__file__))+'/../..'
        condor_exec      = scripts_baseDir + "/server/condor_submit.sh"
        jobOutputDir = scripts_baseDir
    else:
        # Need to add condition here in case path is different for non-jlab
        scripts_baseDir  = "/group/clas12/SubMit"
        condor_exec      = scripts_baseDir + "/server/condor_submit.sh"




    if args.lite:
        dbType = "Test SQLite DB"
        dbName = "../../utils/CLAS12OCR.db"
    elif args.test_database:
        dbType = "Test MySQL DB"
        dbType = fs.MySQL_Test_DB_Name
    else:
        dbType = "Production MySQL DB"
        dbType = fs.MySQL_Prod_DB_Name
    
    print(dbType)
    print(dbName)

    print("submitting job, output going to {0}".format(jobOutputDir))
    url = scard.generator if scard.genExecutable == "Null" else 'no_download'


    #which condor_submit if val = 0, do not submit, print not found message

    # don't know how to pass farmsubmissionID (4th argument), passing GcardID for now (it may be the same)
    # error: we really need to pass farmsubmissionID
    print("trying to submit job now")
    #print([condor_exec, scripts_baseDir, jobOutputDir, params['username'],
    #                 str(usub_id), url, dbType, dbName])
    submission = Popen([condor_exec, scripts_baseDir, jobOutputDir, params['username'],
                      str(usub_id), url, dbType, dbName], stdout=PIPE).communicate()[0]



    print(submission)

    words = submission.split()
    node_number = words[len(words)-1] # This might only work on SubMIT

    timestamp = utils.gettime()
    update_tables.update_farm_submissions(usub_id, timestamp, node_number,
                                        db_conn, sql)
