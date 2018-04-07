import os
#db
db = {
    'hostname':'192.168.1.51',
    'dbName':'db_test',
    'user':'test1',
    'password':'test1',
    'hwTable':'hardware'
}

bugsApiURL='https://bugs.jst/bugs/gethw/?'
smsGateApiURL='http://nms.kvant-telecom.ru/websms.cgi'

#run srcipt dir
current_file_dir = os.path.dirname(__file__)
logFilePath=os.path.join(current_file_dir, 'monitor.log')

#where store rsyslog file
rsyslogFilePath=os.path.join(current_file_dir, '..\\..\\test\\test.log')

#check rsyslog log file delay
#in seconds
rotateDelay = 30
maxPortDownPerOneScan = 5

#in seconds
#delta time from first port down
deltaTime = 300
#count of port for time deltaTime neet to down for trigger
minimumPortDownCount = 5
###

LogLevel="INFO"

#trigger config
triggerDelay = 30
trigerLogFile = os.path.join(current_file_dir, 'trigger.log')
cityWhiteList = ["Нововоронеж", "Губкин"]
phoneList = [""]
