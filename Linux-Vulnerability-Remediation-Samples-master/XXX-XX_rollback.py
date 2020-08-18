# Problem : File Permissions (passwd, shadow and group) Are Not Properly Set
# Jira Tracking ID : XXX-XX
# Objective : The script restores the File Permission using .acl files.
# Note:
# 1. The user running the script must have administrative(root) privileges.
# 2. The script is written in python 2.
# 3. Run this .py script if you wish to rollback the XXX-XX.py solution.
# 4. This _rollback.py script will restore the file permissions changed by XXX-XX.py.
# {

# modifying the file permissions for owner, groups, others  
import os, datetime, sys, time, re 

odat = (time.strftime("%d-%m-%Y"))
dat = datetime.datetime.now()

file_log = '/tmp/XXX-XX_VulnerabilityFix_' + str(odat) + '.log'
f = open(file_log,'a+')
saveout = sys.stdout
sys.stdout = f
print "***************Log Started for XXX-XX_rollback*******************"
os.chdir("/")
os.system("setfacl --restore=/etc/group.acl")
os.system("setfacl --restore=/etc/passwd.acl")
os.system("setfacl --restore=/etc/shadow.acl")
print "File permissions are restored"
print '\n'+str(dat)+'\n'
print 'Updated access permissions:\n'
p1 = os.popen("ls -l /etc/passwd")
print p1.readline()
p2 = os.popen("ls -l /etc/shadow")
print p2.readline()
p3 = os.popen("ls -l /etc/group")
print p3.readline()
print "***************Log Ended for XXX-XX_rollback*******************"
sys.stdout = saveout
f.close()
print "Message: Check log file at: ", file_log
print "Message: Check .acl files at: /etc/"
#}

'''
# Log file at /tmp/XXX-XX_VulnerabilityFix_29-03-2018.log is:

***************Log Started for XXX-XX_rollback*******************
File permissions are restored

2018-03-29 22:51:18.549713

Updated access permissions:

-rwxrwxrwx. 1 root root 2613 Jan 22 00:31 /etc/passwd

-rwxrwxrwx. 1 root root 1391 Jan 22 00:31 /etc/shadow

-rwxrwxrwx. 1 root root 1062 Feb 22 10:12 /etc/group

***************Log Ended for XXX-XX_rollback*******************
'''
