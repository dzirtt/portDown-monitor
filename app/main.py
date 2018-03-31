import config as cfg
import sys, bugsapi, utils, os, db_worker,sql_templates
import logging as log
import log_parser
from pathlib import Path


def main():
    initLogging()

    #rsyslog file exist
    if not Path(cfg.rsyslogFilePath).is_file():
        log.error('file {0} not exist'.format(cfg.rsyslogFilePath))
        sys.exit(1)

    #check and init db tables
    returnCode = checkAndInitDB()
    if returnCode > 0 :
        sys.exit(returnCode)

    #hwIds = rsyslogFileWork(cfg.rsyslogFilePath)
    #print(len(hwIds))
    #db_worker.updateDb(hwIds)

    data = db_worker._testQuery(sql_templates.select_hw_by_id,"10")
    print(data[0][0:3])
    #get file, split by line, extract id\ip, upload to bd

    sys.exit(0)

def getHwData(ip_or_id):
    data = bugsapi.getData(ip_or_id)
    return data

def initLogging():
    log.basicConfig(filename=cfg.logFilePath,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
    #alose log to std out
    log.getLogger().addHandler(log.StreamHandler())

def rsyslogFileWork(logFilePath):
    hwLogs = log_parser.parseAndCleanFile(logFilePath)
    hwIdsOnly = []

    for line in hwLogs:
        try:
            hw = line.split(' ')[3]
            if(utils.isIpOrId(hw)):
                hwIdsOnly.append(hw)
        except:
            log.warning('cant parse line "{0}"'.format(line))
            raise

    return hwIdsOnly

def checkAndInitDB():
    if db_worker.testDBConnection():
        if not db_worker.tableIsExist(cfg.db["hwTable"]):
            if not db_worker.createTable(sql_templates.create_hardware_table):
                log.error("cant create new hardware table from template '{0}''".format('create_hardware_table'))
                return 2
            else:
                log.info("create new table hardware frrom template '{0}''".format('create_hardware_table'))
    else:
        log.error("cant connect to db with {0}".format(cfg.db))
        return 2

    return 0

if __name__ == "__main__":
    main()
