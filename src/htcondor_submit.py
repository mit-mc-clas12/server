"""

Submit a job using htcondor.

"""



import os
import sys
from subprocess import PIPE, Popen

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../utils')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../utils/scripts')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../submission_files')
import fs
from job_counter import shouldBeSubmitted
import update_tables
import utils


def htcondor_submit(args, scard, usub_id, file_extension, params, db_conn, sql, idle_limit=20000):

    #Test to see if user has too many jobs currently running:
    #shouldBeSubmitted will return false if number of jobs for that user is over idle limit
    if not shouldBeSubmitted(params['username'],idle_limit=idle_limit):
        print("user is over limit for number of jobs, changing run_status to 'waiting to submit'")
        timestamp = utils.gettime()
        update_tables.update_farm_submission_to_waiting(usub_id, timestamp,db_conn, sql)
        return 1 

    jobOutputDir = args.OutputDir

    if args.OutputDir == "TestOutputDir":
        print("Test output dir specified")
        jobOutputDir = os.path.dirname(os.path.abspath(__file__))+'/../..'

    if args.test_condorscript:
        scripts_baseDir  = os.path.dirname(os.path.abspath(__file__))+'/../..'
        condor_exec      = scripts_baseDir + "/server/condor_submit.sh"
    else:
        # Need to add condition here in case path is different for non-jlab
        scripts_baseDir  = "/home/gemc/software/Submit/"
        condor_exec      = scripts_baseDir + "/server/condor_submit.sh"

    if args.lite:
        dbType = "Test SQLite DB"
        dbName = "../../utils/CLAS12OCR.db"
    elif args.test_database:
        dbType = "Test MySQL DB"
        dbName = fs.MySQL_Test_DB_Name
        scripts_baseDir  = "/home/gemc/software/Submit/test"

    else:
        dbType = "Production MySQL DB"
        dbName = fs.MySQL_Prod_DB_Name
    
    print(dbType)
    print(dbName)

    print("submitting job, output going to {0}".format(jobOutputDir))
    url = scard.generator if scard.genExecutable == "Null" else 'no_download'


    #The following is useful for testing on locations which do not have htcondor installed
    #This allows us to go all the way through with condor_submit.sh even if htcondor does not exist
    htcondor_version = Popen(['which', 'condor_submit'], stdout=PIPE).communicate()[0]
    if not htcondor_version:
        htcondor_present="no"
    else:
        htcondor_present="yes"

    print(htcondor_present)

    if args.submit:

        # don't know how to pass farmsubmissionID (4th argument), passing GcardID for now (it may be the same)
        # error: we really need to pass farmsubmissionID
        print("trying to submit job now")
        #print([condor_exec, scripts_baseDir, jobOutputDir, params['username'],
        #                 str(usub_id), url, dbType, dbName])
        #Note: Popen array arguements must only contain strings
        submission = Popen([condor_exec, scripts_baseDir, jobOutputDir, params['username'],
                        str(usub_id), url, dbType, dbName, str(htcondor_present)], stdout=PIPE).communicate()[0]



        print(submission.decode('ascii'))

        words = submission.decode('ascii').split()
        node_number = words[len(words)-1] # This might only work on SubMIT

        timestamp = utils.gettime()
        update_tables.update_farm_submissions(usub_id, timestamp, node_number,
                                            db_conn, sql)

    else:
        print("-s option not selected, not passing jobs to condor_submit.sh")

if __name__ == "__main__":
    print("Trying a test submission on htcondor_submit.py")
