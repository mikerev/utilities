#!/usr/bin/env python
# 
# Requires s3cmd and respective bucket info, as well as mysqldump. On Ubuntu 
# 14.04/16.06: apt-get install s3cmd mysql-
import subprocess, datetime, socket
from sys import argv

script, switch = argv

# Define mysqldump vars
dbuser = "backups"
dbpass = "3l1t3p455w0rd"
dbs = ['some.dbserver']

# Define a target dir to backup
target_path = "/opt/somedir/"


tmpdir = "/data/backups"
tstamp = datetime.datetime.now().strftime('%m-%d-%Y-%H%M%S')
host = socket.gethostname()
config = "--config /root/.s3cfg"

def dbJob():
    file_name = 'mysql-%s-%s.sql' % (host, tstamp)
    file_path = '%s/%s' % (tmpdir, file_name)
    dumper = 'mysqldump -u %s -p%s > %s' % (dbuser, dbpass, file_path)
    sender = 's3cmd sync --check-md5 %s s3://backups.tastyworks.internal/mysql/%s %s-mysql' % (file_path, file_name, config)
    subprocess.call(dumper, shell=True)
    subprocess.call(sender, shell=True)


def fileJob():
    sender = 's3cmd sync --check-md5 %s s3://backups.tastyworks.internal/file/%s/%s/ %s-file' % (target_path, host, tstamp, config)
    subprocess.call(sender, shell=True)

if switch == 'all':
    dbJob()
    fileJob()
elif switch == 'dbs':
    dbJob()
elif switch == 'files':
    fileJob()
else:
  print 'Invalid argument. Expecting ./s3sync (all|dbs|files)'
