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
import os
import sqlite3
import subprocess
import sys
import time

# this project
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) \
                + '/../../utils')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) \
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

    if args.UserSubmissionID != 'none':
        if count_user_submission_id(args.UserSubmissionID) > 0:
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
            logger.debug('Found unsubmitted jobs:', user_submissions)

            if len(user_submissions) == 0:
                print("There are no UserSubmissions which have not yet been submitted to a farm")

            else:
                for submission_id in user_submissions:
                    utils.printer("Generating scripts for UserSubmission with UserSubmissionID = {0}".format(
                        str(submission_id)))
                    submission_script_manager.process_jobs(args, submission_id, db_conn, sql)

    # Shutdown the database, we're done here.
    db_conn.close()

def count_user_submission_id(user_sub_id):
    """ Select and count instances of the UserSubmissionID and
    return a count.

    Inputs:
    -------
    - user_sub_id - (int) From UserSubmissions.UserSubmissionID

    Returns:
    --------
    - count - (int) Total number of submissions with this ID.
    We really only ever care about 0 and 1.  There shouldn't
    be more than 1.
    """

    query = """
    SELECT COUNT(UserSubmissionID) FROM UserSubmissions
        WHERE UserSubmissionID = {0};
    """.format(user_sub_id)

    count = utils.db_grab(query)

    # The database call returns an array with a tuple inside of it
    # so we need the first element of each.
    return int(count[0][0])

if __name__ == "__main__":
    args = get_args.get_args()
    Submit_UserSubmission(args)
