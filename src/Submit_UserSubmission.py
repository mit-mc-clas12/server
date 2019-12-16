"""
This file will query the command line to see what UserSubmissionID it should use,
or if no arguement is given on the CL, the most recent UserSubmissionID will be used
This UserSubmissionID is used to identify the proper scard and gcards, and then submission
files corresponding to each gcard are generated and stored in the database, as
well as written out to a file with a unique name. This latter part will be passed
to the server side in the near future.

"""

from __future__ import print_function

# python standard lib
import argparse
import os
import sqlite3
import subprocess
import sys
import time

# this project
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))
                + '/../../utils')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))
                + '/../submission_files')
import database
import farm_submission_manager
import fs
import get_args
import lund_helper
import scard_helper
import script_factory
import submission_script_manager
import update_tables
import utils


def Submit_UserSubmission(args):

    logger = utils.configure_logger(args)

    # Setup database authentication, connect to database.
    cred_file = os.path.normpath(
        os.path.dirname(os.path.abspath(__file__)) + '/../../msqlrw.txt'
    )
    username, password = database.load_database_credentials(cred_file)
    use_mysql = False if args.lite else True

    logger.debug('Connecting to MySQL: {}'.format(
        use_mysql))

    if args.lite is not None:
        database_name = args.lite 
    else:
        if args.test_database:
            database_name = "CLAS12TEST"
        else:
            database_name = "CLAS12OCR"

    db_conn, sql = database.get_database_connection(
        use_mysql=use_mysql,
        database_name=database_name,
        username=username,
        password=password,
        hostname='jsubmit.jlab.org'
    )

    # purge_old_jobs(db_conn, sql, hours=1)

    if args.UserSubmissionID != 'none':
        if update_tables.count_user_submission_id(args.UserSubmissionID, sql) > 0:
            logger.debug('Processing {}'.format(args.UserSubmissionID))
            submission_script_manager.process_jobs(args, args.UserSubmissionID, db_conn, sql)
        else:
            print("The selected UserSubmission (UserSubmissionID = {0}) does not exist, exiting".format(
                args.UserSubmissionID))
            exit()

    # No UserSubmissionID specified, send all
    # that haven't been sent already.
    else:
        if args.submit:
            user_submissions = database.get_unsubmitted_jobs(sql)
            logger.debug('Found unsubmitted jobs: {}'.format(user_submissions))

            if len(user_submissions) == 0:
                print("There are no UserSubmissions which have not yet been submitted to a farm")

            else:
                for i, submission_id in enumerate(user_submissions):
                    logger.debug('Working on job {} of {}, user_submission_id = {}'.format(
                        i + 1, len(user_submissions), submission_id
                    ))
                    submission_script_manager.process_jobs(args, submission_id, db_conn, sql)

    # Shutdown the database, we're done here.
    db_conn.close()

def configure_args():

    parser = argparse.ArgumentParser()
    
    help_str = "Enter the ID# of the batch you want to submit (e.g. -b 23)"
    parser.add_argument('-b','--UserSubmissionID', default='none', help=help_str)

    help_str = ("Use this flag (no arguments) if you are NOT on a farm"
                " node and want to test the submission flag (-s)")
    parser.add_argument('-t', '--test', help = help_str, action = 'store_true')

    help_str = "Use this flag (no arguments) if you want to submit the job"
    parser.add_argument('-s', '--submit', help=help_str, action='store_true')

    help_str = ("Use this flag (no arguments) if you want submission "
                "files to be written out to text files")
    parser.add_argument('-w','--write_files', help=help_str, 
                        action='store_true')

    help_str = "Enter scard type (e.g. -y 1 for submitting type 1 scards)"
    parser.add_argument('-y','--scard_type', default='0', help =help_str)

    help_str = ("use -l or --lite to connect to sqlite DB, "
                "otherwise use MySQL DB")
    parser.add_argument('-l','--lite', help=help_str, type=str, default=None)

    help_str =  ("Enter full path of your desired output directory, "
                 "e.g. /u/home/robertej")
    parser.add_argument('-o','--OutputDir', default='none', help=help_str)

    help_str = "Use testing database (MySQL)"
    parser.add_argument('--test_database', action='store_true', 
                        default=False, help=help_str)

    help_str = fs.debug_help
    parser.add_argument(fs.debug_short,fs.debug_longdash, 
                        default=fs.debug_default, help=help_str)

    args = parser.parse_args()
    
    fs.DEBUG = getattr(args, fs.debug_long)
    fs.use_mysql = False if args.lite else True

    return args

def purge_old_jobs(db_conn, sql, hours):
    for job in database.get_old_jobs_from_queue(sql, hours):
        update_tables.purge_old_job_from_queue(db_conn, sql, job)        

if __name__ == "__main__":
    args = configure_args()
    Submit_UserSubmission(args)
