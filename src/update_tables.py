"""

This module contains methods that update tables
from the server side.  Anything that uses an 
INSERT or UPDATE call on the server should be here. 

"""

import logging

def update_run_script(field_name, script_text, gcard_id, db_conn, sql):
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

    strn = 'UPDATE FarmSubmissions SET {0} = "{1}" WHERE GcardID = {2};'.format(
        field_name, script_text, gcard_id)
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

    strn = "UPDATE FarmSubmissions SET run_status = '{0}' WHERE UserSubmissionID = {1};".format(
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
    SELECT Total_UserSubmissions FROM Users
    WHERE User = {}
    """.format(params['username'])
    logger.debug('Executing SQL command: {}'.format(query))

    sql.execute(query)
    total = sql.fetchall()[0][0]
    total += 1 

    # Update the total submissions for our user
    strn = """
    UPDATE Users SET Total_UserSubmissions = '{0}' 
    WHERE User = '{1}';""".format(
        UserSubmissions_total, params['username'])
    logger.debug('Executing SQL command: {}'.format(strn))

    sql.execute(strn)

    if 'nevents' in scard.data:
        query = """
        SELECT Total_Events FROM Users 
        WHERE User = '{0}';""".format(params['username'])
        sql.execute(query)
        events_total = sql.fetchall()[0][0]
        events_total += int(scard.data['jobs']) * int(scard.data['nevents'])
        
        strn = """
        UPDATE Users SET Total_Events = '{0}' 
        WHERE User = '{1}';""".format(
            events_total, params['username'])
        logger.debug('Executing SQL command: {}'.format(strn))
        sql.execute(strn)

    strn = """
    UPDATE Users SET Most_Recent_Active_Date = '{0}' 
    WHERE User = '{1}';""".format(
        timestamp, params['username'])
    logger.debug('Executing SQL command: {}'.format(strn))
    sql.execute(strn)
    db_conn.commit() 
