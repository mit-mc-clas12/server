"""

The server handles the submission
of unsubmitted jobs from the
database to the OSG.

"""

from __future__ import print_function

# python standard lib
import argparse
import logging
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
import script_factory
import submission_script_manager
import update_tables
import utils


def server(args):
    """
    Server function to drive the submission process.  Two main modes
    of operation are present.  First, user submissions can be directly
    submitted with the -b flag.  This is mainly used for debugging.
    The main mode of operation is without the -b flag, where the server
    will check the database for jobs that haven't been submitted and call
    submission_script_manager for each.

    Inputs:
    ------
    args - argparse arguments object that contains the database
    configuration instructions as well as other options.

    Returns:
    --------
    Nothing. For a more verbose output, use --debug=2 at the
    runtime.

    """

    logger = utils.configure_logger(args)
    db_conn, sql = setup_database(args)

    if args.UserSubmissionID != 'none':
        if update_tables.count_user_submission_id(args.UserSubmissionID, sql) > 0:
            #if args.submit:     
                logger.debug('Processing {}'.format(args.UserSubmissionID))

                #Need to remove any whitespace
                USID = args.UserSubmissionID.replace(" ","")

                submission_script_manager.process_jobs(args, args.UserSubmissionID, db_conn, sql)
            #else:
                #print("-s option not selected, not submitting jobs through submission_script_manager")
        else:
            print("The selected UserSubmission (UserSubmissionID = {0}) does not exist, exiting".format(
                args.UserSubmissionID))
            exit()

    # No UserSubmissionID specified, send all
    # that haven't been sent already.
    else:
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

    # Shutdown the database connection, we're done here.
    db_conn.close()

def configure_args():
    """ Setup the parser and get the options
    this user has passed to us.  """
    parser = argparse.ArgumentParser()

    help_str = "Enter the ID# of the batch you want to submit (e.g. -b 23)"
    parser.add_argument('-b','--UserSubmissionID', default='none', help=help_str)

    help_str = ("Use this flag (no arguments) if you are NOT on a farm"
                " node and want to test the submission flag (-s)")
    parser.add_argument('-t', '--test_condorscript', help = help_str, action = 'store_true')

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
    parser.add_argument('-o','--OutputDir', default="/volatile/clas12/osg", help=help_str)

    help_str = "Use testing database (MySQL)"
    parser.add_argument('--test_database', action='store_true',
                        default=False, help=help_str)

    help_str = fs.debug_help
    parser.add_argument(fs.debug_short,fs.debug_longdash,
                        default=fs.debug_default, help=help_str)

    return parser.parse_args()

def setup_database(args):
    """ Setup database connection based on command line
    options.
    """
    logger = logging.getLogger('SubMit')


    if args.lite:
        use_mysql = False
        username, password = "none", "none"
        database_name = args.lite
    else:
        use_mysql = True
        if args.test_database:
            cred_file_name = '/..'+fs.test_db_cred_file #the ../ is needed due to the path difference in client/src and utils/
            database_name = fs.MySQL_Test_DB_Name
        else:
            cred_file_name = '/..'+fs.prod_db_cred_file
            database_name = fs.MySQL_Prod_DB_Name
            
        cred_file_loc = os.path.dirname(os.path.abspath(__file__)) + cred_file_name
        cred_file = os.path.normpath(cred_file_loc)
        username, password = database.load_database_credentials(cred_file)






    logger.debug('Connecting to MySQL: {}'.format(
        use_mysql))

    db_conn, sql = database.get_database_connection(
        use_mysql=use_mysql,
        database_name=database_name,
        username=username,
        password=password,
        hostname=fs.db_hostname
    )

    return db_conn, sql

if __name__ == "__main__":
    server(configure_args())
