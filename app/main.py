import config as cfg
import sys, bugsapi, utils, os, db_worker
import logging as log
import log_parser
from pathlib import Path



def main():
    initLogging()

    if not Path(cfg.rsyslogFilePath).is_file():
        log.error('file {0} not exist'.format(cfg.rsyslogFilePath))
        sys.exit(1)

    hwIds = rsyslogFileWork(cfg.rsyslogFilePath)

    #db_worker.updateDb(hwIds)
    db_worker.testDBConnection()
    print(db_worker.tableIsExist(cfg.db["hwTable"]))

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
            hwIdsOnly.append(line.split( )[3])
        except:
            log.warning('cant parse lise "{0}"'.format(line))

    return hwIdsOnly


if __name__ == "__main__":
    main()
