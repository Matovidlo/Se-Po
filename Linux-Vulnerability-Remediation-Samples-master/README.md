# Linux-Vulnerability-Remediation-Samples-Python
Sample code for Remediating Common Vulnerabilities in Linux Machines

1. Single Script for fixing, rollback and logging.

  XXX-XX.py 
  -   It is a remediation script for setting appropriate File Permissions to /etc/shadow, /etc/passwd and /etc/group files.
  
  XXX-XX_rollback.py 
  -   It is a rollback script for reverting the changes made by XXX-XX.py using the logs and .acl backup files.

2. Modular Scripts for Searching files (.xml or .conf) in complete '/' directory and then making necesary changes alongwith logging. The priority is given here to separation of concerns such that code reusability can be achieved for different config file related vulnerability remediations.[ Here the issue is regarding 'Security Headers Not Found' in the web requests/responses ]

  YYYY-YY-curr_dt.py 
  -   This module is developed to get current date and time separately from the system.

  YYYY-YY-find_path.py 
  -   This module is designed to find the path of necessary files to be edited.
  -   To initialise the entries to be made in the file.
  -   To devise a backup strategy for the file to be edited.

  YYYY-YY-dec_ins.py
  -   This module is developed with the help of decorator pattern to make suitable changes in the conf files.

  YYYY-YY-dec_log.py
  -   This module is reponsible for appropriate logging of Linux Details, Changes made in the conf file and Backup info.

  YYYY-YY-rollback.py
  -   This module will revert all the changes made by YYYY-YY.py modules.
