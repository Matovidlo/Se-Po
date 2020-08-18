####################
### find_path.py ###
####################

# Vulnerability: Security Header not detected.
# Solution: Adding Security Header entries in server config files
# This module of solution will find all the server .conf files whether http or apache, irrespective of Linux OS.

import os
from curr_dt import *


def find_path():
        f_found = []
        conf_file_name = ["apache.conf", "apache2.conf", "httpd.conf"]
        for root, dirs, files in os.walk(r'/'):
                for name in files:
                        if name in conf_file_name:
                                print "Name of file found is: ", name
                                z = os.path.abspath(os.path.join(root, name))
                                f_found.append(z)
        return f_found


def lf():
    list_find = ['Header always append X-Frame-Options SAMEORIGIN',
                 'Header set X-XSS-Protection "1; mode=block"',
                 'Header set X-Content-Type-Options nosniff',
                 'Header set Content-Security-Policy "default-src \'self\';"']
    return list_find


def backup(x):
        # print "\n\nComplete path of File Found is : ", x
        # In 'y' give the VRG number as depicted in Jira
        y = '.XXX-XX.' + str(cur_date())
        back_up = x + y

        if not os.path.isfile(back_up):
            print "\nComplete path of File Found is : ", x
            os.system('cp ' + x + ' ' + back_up)
            print "Backup file of " + x + " is created at: " + back_up
        else:
            print "\nBackup already present for " + x

