##################
### dec_log.py ###
##################

import sys
from dec_ins import *


def my_decorator(func):
    @functools.wraps(func)
    def function_that_runs_func():

        # Check whether tmp dir exists or not
        if not os.path.exists('/tmp'):
            print "/tmp directory is not there, so creating /tmp"
            os.makedirs('/tmp')

        # Create appropriate log file
        file_log = '/tmp/YYYY-YY_VulnerabilityFix_' + str(cur_date()) + '.log'
        f = open(file_log, 'a+')
        save_out = sys.stdout
        sys.stdout = f
        print "**************************Log Started for YYYY-YY********************************"
        linux_check = (os.popen("uname -a").readlines())
        linux_check = ''.join(linux_check)
        print "Linux Details: ", linux_check

        func()

        print '\n'+str(cur_time())+'\n'
        print "Message: Check log files at: ", file_log
        print "Message: Please restart the service manually..."

        print "**************************Log Ended for YYYY-YY**********************************"

        sys.stdout = save_out
        f.close()

        # Guidelines printed after script run
        # print "Backup for the .conf as .conf.bkp is created as: ", bkp
        print "Log file created at: ", file_log
        print "Please restart the Server manually"

    return function_that_runs_func


@my_decorator
def my_function():
    f_found = find_path()
    if len(f_found) == 0:
        print "File not found..."
    else:
        dec_ins(f_found)


my_function()
