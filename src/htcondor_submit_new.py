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

    # Need to add condition here in case path is different for non-jlab
    scripts_baseDir  = "/group/clas12/SubMit"
    condor_exec      = scripts_baseDir + "/server/condor_submit.sh"
    #jobOutputDir     = "/volatile/clas12/osg"
    jobOutputDir = "/u/home/robertej"
    url = scard.generator if scard.genExecutable == "Null" else 'no_download'

    # don't know how to pass farmsubmissionID (4th argument), passing GcardID for now (it may be the same)
    # error: we really need to pass farmsubmissionID
    print("trying to submit job now")
    submission = Popen([condor_exec, scripts_baseDir, jobOutputDir, params['username'],
                      str(usub_id), url], stdout=PIPE).communicate()[0]

    print("sub is")
    print(submission)
    print("end sub")
    # what is this?
    words = submission.split()
    node_number = words[len(words)-1] # This might only work on SubMIT

    timestamp = utils.gettime()
    update_tables.update_farm_submissions(usub_id, timestamp, node_number,
                                        db_conn, sql)
