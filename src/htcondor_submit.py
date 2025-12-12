"""
Submit a job using htcondor.
"""

import os
import sys
import re
from subprocess import Popen, PIPE, STDOUT

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../../utils')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../../utils/scripts')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../submission_files')

import fs
from job_counter import shouldBeSubmitted
import update_tables
import utils


def run_condor_and_get_output(cmd, debug_tag="condor_submit"):
    """
    Run condor_submit wrapper, stream output to stderr, and capture it.
    """
    print(f"[DEBUG {debug_tag}] Running: {' '.join(cmd)}", file=sys.stderr)

    proc = Popen(
        cmd,
        stdout=PIPE,
        stderr=STDOUT,
        universal_newlines=True  # works on older Python instead of text=True
    )

    output_lines = []

    for line in proc.stdout:
        # Show submit output live (to stderr so it appears with the traceback/logs)
        sys.stderr.write(line)
        output_lines.append(line)

    proc.wait()
    full_output = "".join(output_lines)

    # Also dump to a temp file for later inspection
    try:
        log_dir = "/home/gemc/log"
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)
        log_path = os.path.join(log_dir, f"{debug_tag}.log")
        with open(log_path, "w") as f:
            f.write(full_output)
        print(f"[DEBUG {debug_tag}] Full output logged to {log_path}", file=sys.stderr)
    except Exception as e:
        print(f"[DEBUG {debug_tag}] Failed to write debug log: {e}", file=sys.stderr)

    return proc.returncode, full_output


def extract_cluster_id(full_output):
    """
    Try to extract the HTCondor cluster id from condor_submit output.

    Returns:
        int cluster_id

    Raises:
        RuntimeError if no cluster id can be confidently determined.
    """
    # Standard pattern:
    #   "X job(s) submitted to cluster 5842."
    patterns = [
        r"submitted to cluster\s+(\d+)",   # canonical
        r"cluster\s+(\d+)\.",             # e.g. "cluster 5842."
        r"cluster\s+(\d+)\b",             # generic 'cluster 5842'
    ]

    for pat in patterns:
        m = re.search(pat, full_output, re.IGNORECASE)
        if m:
            return int(m.group(1))

    # If you really want a "last number" fallback, uncomment:
    # nums = re.findall(r"\b(\d+)\b", full_output)
    # if nums:
    #     return int(nums[-1])

    raise RuntimeError(
        "condor_submit succeeded but cluster id not found.\n"
        "Full output was:\n"
        f"{full_output}"
    )


def htcondor_submit(args, scard, usub_id, file_extension, params, db_conn, sql, idle_limit=80000):
    # Test to see if user has too many jobs currently running:
    # shouldBeSubmitted will return false if number of jobs for that user is over idle limit
    if not shouldBeSubmitted(params['username'], idle_limit=idle_limit):
        print("user is over limit for number of jobs, changing run_status to 'waiting to submit'")
        timestamp = utils.gettime()
        update_tables.update_farm_submission_to_waiting(usub_id, timestamp, db_conn, sql)
        return 1

    jobOutputDir = args.OutputDir

    if args.OutputDir == "TestOutputDir":
        print("Test output dir specified")
        jobOutputDir = os.path.dirname(os.path.abspath(__file__)) + '/../..'

    if args.test_condorscript:
        scripts_baseDir = os.path.dirname(os.path.abspath(__file__)) + '/../..'
        condor_exec = scripts_baseDir + "/server/condor_submit.sh"
    else:
        # Need to add condition here in case path is different for non-jlab
        scripts_baseDir = "/home/gemc/software/Submit/"
        condor_exec = scripts_baseDir + "/server/condor_submit.sh"

    if args.lite:
        dbType = "Test SQLite DB"
        dbName = "../../utils/CLAS12OCR.db"
    elif args.test_database:
        dbType = "Test MySQL DB"
        dbName = fs.MySQL_Test_DB_Name
        scripts_baseDir = "/home/gemc/software/Submit/test"
        condor_exec = scripts_baseDir + "/server/condor_submit.sh"
    else:
        dbType = "Production MySQL DB"
        dbName = fs.MySQL_Prod_DB_Name

    print(dbType)
    print(dbName)

    print("Submitting job, output going to {0}".format(jobOutputDir))
    url = scard.generator if scard.genExecutable == "Null" else 'no_download'

    # The following is useful for testing on locations which do not have htcondor installed
    # This allows us to go all the way through with condor_submit.sh even if htcondor does not exist
    htcondor_version = Popen(['which', 'condor_submit'], stdout=PIPE).communicate()[0]
    if not htcondor_version:
        htcondor_present = "no"
    else:
        htcondor_present = "yes"

    print(htcondor_present)

    if args.submit:
        print("trying to submit job now")

        cmd = [
            condor_exec,
            scripts_baseDir,
            jobOutputDir,
            params['username'],
            str(usub_id),
            url,
            dbType,
            dbName,
            str(htcondor_present),
        ]

        # Run condor_submit.sh, stream output, capture for parsing
        retcode, full_output = run_condor_and_get_output(cmd, debug_tag=f"condor_submit_{usub_id}")

        if retcode != 0:
            # Hard failure: propagate up
            raise RuntimeError(
                f"condor_submit failed with exit code {retcode}\n{full_output}"
            )

        # Parse cluster id from output (robust)
        cluster_id = extract_cluster_id(full_output)
        print(f"[DEBUG condor_submit] Parsed cluster_id = {cluster_id}", file=sys.stderr)

        # Update DB as before
        timestamp = utils.gettime()
        update_tables.update_farm_submissions(usub_id, timestamp, cluster_id, db_conn, sql)

    else:
        print("-s option not selected, not passing jobs to condor_submit.sh")


if __name__ == "__main__":
    print("Trying a test submission on htcondor_submit.py")
