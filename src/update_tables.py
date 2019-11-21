"""

This module contains methods that update tables
from the server side.  Anything that uses an 
INSERT or UPDATE call on the server should be here. 

"""

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
    strn = 'UPDATE FarmSubmissions SET {0} = "{1}" WHERE GcardID = {2};'.format(
        field_name, script_text, gcard_id)
    sql.execute(strn)
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
    strn = "UPDATE FarmSubmissions SET run_status = '{0}' WHERE UserSubmissionID = {1};".format(
        submission_string, usub_id)     
    sql.execute(strn)
    db_conn.commit() 
    
