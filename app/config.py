import os
#db
db = {
    'hostname':'192.168.1.65',
    'dbName':'db_test',
    'user':'test1',
    'password':'test1',
    'hwTable':'hardware'
}

bugsApiURL='https://bugs.jst/bugs/gethw/?'

#run srcipt dir
current_file_dir = os.path.dirname(__file__)
logFilePath=os.path.join(current_file_dir, 'monitor.log')

#where store rsyslog file
rsyslogFilePath=os.path.join(current_file_dir, '..\\test\\test.log')

#in seconds
#delta time from first port down
deltaTime = 300
