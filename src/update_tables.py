"""

This module contains methods that update tables
from the server side.  Anything that uses an
INSERT or UPDATE call on the server should be here.

"""

import logging

def update_run_script(field_name, script_text, usub_id, db_conn, sql):
    """ Update runscript text in the FarmSubmissions table.

    Inputs:
    -------
    - field_name - (str) table column name for insertion of the run script
    - script_text - (str) the actual bash script text
    - gcard_id - (int) GcardID for this submission
    - dc_conn - database connection for commiting
    - sql - cursor object for executing database commands

    Returns:
    --------
    Nothing, the database is updated.

    """
    logger = logging.getLogger('SubMit')

    strn = 'UPDATE submissions SET {0} = "{1}" WHERE user_submission_id = {2};'.format(
        field_name, script_text, usub_id)
    sql.execute(strn)
    logger.debug('Executing SQL statement: {}'.format(strn))
    db_conn.commit()

def update_run_status(submission_string, usub_id, db_conn, sql):
    """ Update the run_status variable in the FarmSubmissions table.

    Inputs:
    -------
    - submission_string - (str) current submission status
    - usub_id - (int) UserSubmissionID for this entry
    - dc_conn - database connection for commiting
    - sql - cursor object for executing database commands

    Returns:
    --------
    Nothing, the database is updated.

    """
    logger = logging.getLogger('SubMit')

    strn = "UPDATE submissions SET run_status = '{0}' WHERE user_submission_id = {1};".format(
        submission_string, usub_id)
    sql.execute(strn)
    logger.debug('Executing SQL statement: {}'.format(strn))
    db_conn.commit()

def update_users_statistics(scard, params, timestamp, db_conn, sql):
    """ After submission, the user statistics from the Users
    table are updated.

    Inputs:
    -------
    - scard - (scard_class) The current submission card
    - params - (dict) parameters of the current submission
    - db_conn - database connection, for committing changes
    - sql - database cursor, for execution of statements

    Returns:
    --------
    - Nothing, the database is modified

    """

    logger = logging.getLogger('SubMit')

    query = """
    SELECT total_submissions FROM users
    WHERE user = '{}'
    """.format(params['username'])
    logger.debug('Executing SQL command: {}'.format(query))

    sql.execute(query)
    total = sql.fetchall()[0][0]
    total += 1

    # Update the total submissions for our user
    strn = """
    UPDATE users SET total_submissions = '{0}'
    WHERE user = '{1}';""".format(
        total, params['username'])
    logger.debug('Executing SQL command: {}'.format(strn))

    sql.execute(strn)

    if 'nevents' in scard.data:
        query = """
        SELECT total_events FROM users
        WHERE user = '{0}';""".format(params['username'])
        sql.execute(query)
        events_total = sql.fetchall()[0][0]
        events_total += int(scard.data['jobs']) * int(scard.data['nevents'])

        strn = """
        UPDATE users SET total_events = '{0}'
        WHERE user = '{1}';""".format(
            events_total, params['username'])
        logger.debug('Executing SQL command: {}'.format(strn))
        sql.execute(strn)

    #strn = """
    #UPDATE users SET most_recent_active_date = '{0}'
    #WHERE user = '{1}';""".format(
    #    timestamp, params['username'])
    #logger.debug('Executing SQL command: {}'.format(strn))
    #sql.execute(strn)
    db_conn.commit()

def update_farm_submissions(usub_id, timestamp, node_number, db_conn, sql):
    """ After submission, update FarmSubmissions
    with the node number and timestamp.

    Inputs:
    -------
    - GCardID (int) - The gcard_id for this submission
    - timestamp - Submission time
    - node_number - Node number (need to understand this)
    - db_conn - database connection for committing changes
    - sql - database cursor for executing statements

    Returns:
    --------
    Nothing, the database is modified

    """
    strn = ("UPDATE submissions SET run_status "
            "= 'submitted to pool' WHERE user_submission_id = '{0}';").format(usub_id)
    sql.execute(strn)
    strn = ("UPDATE submissions SET server_time"
            " = '{0}' WHERE user_submission_id = '{1}';").format(timestamp, usub_id)
    sql.execute(strn)

    strn = ("UPDATE submissions SET pool_node "
            "= '{0}' WHERE user_submission_id = '{1}';").format(node_number, usub_id)
    sql.execute(strn)
    db_conn.commit()

def count_user_submission_id(user_sub_id, sql):
    """ Select and count instances of the UserSubmissionID and
    return a count.

    Inputs:
    -------
    - user_sub_id - (int) From UserSubmissions.UserSubmissionID
    - sql - cursor object to execute database query

    Returns:
    --------
    - count - (int) Total number of submissions with this ID.
    We really only ever care about 0 and 1.  There shouldn't
    be more than 1.
    """

    query = """
    SELECT COUNT(user_submission_id) FROM submissions
        WHERE user_submission_id = {0};
    """.format(user_sub_id)
    sql.execute(query)
    count = sql.fetchall()[0][0]

    return int(count)
