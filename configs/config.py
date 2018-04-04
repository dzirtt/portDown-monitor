import os
#db
db = {
    'hostname':'127.0.0.1',
    'dbName':'portmonitor',
    'user':'monitor',
    'password':'monitor',
    'hwTable':'hardware'
}

bugsApiURL='https://bugs.jst/bugs/gethw/?'
smsGateApiURL='http://nms.kvant-telecom.ru/websms.cgi'

#run srcipt dir
current_file_dir = os.path.dirname(__file__)
#logFilePath=os.path.join(current_file_dir, 'monitor.log')
logFilePath='/var/log/monitor/port.log'

#where store rsyslog file
#rsyslogFilePath=os.path.join(current_file_dir, '..\\test\\test.log')
rsyslogFilePath='/var/log/monitor/monitor.log'

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
#trigerLogFile = os.path.join(current_file_dir, 'trigger.log')
trigerLogFile = '/var/log/monitor/trigger.log'
cityWhiteList = ["Нововоронеж"]
phoneList = ["79065869848"]

