import config as cfg
import sys, bugsapi, utils, os, db_worker,sql_templates
import time
from datetime import datetime, timedelta
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
    returnCode = db_worker.checkAndInitTable()
    if returnCode > 0 :
        sys.exit(returnCode)

    count = 0
    now = datetime.now()
    hw_ids = log_parser.rsyslogFileWork(cfg.rsyslogFilePath)
    for id in hw_ids:
        result = getHwFromDbOrInsertNew(id, now)
        if result == None:
            continue

        portDownDate = result[3]
        deltaInSeconds = (now - portDownDate).total_seconds()

        #delta < 0 its may be error in app. or wrong date on server betwen app starts
        if deltaInSeconds > cfg.deltaTime or deltaInSeconds < 0:
            log.debug("reset counter, current deltaTime: {0}, cfg.deltaTime: {1}".format(deltaInSeconds, cfg.deltaTime))
            args=(1, now, id)
            if utils.isIp(id):
                state = db_worker.setQuery(sql_templates.update_by_ip, args)
            else:
                state = db_worker.setQuery(sql_templates.update_by_id, args)



    print(count)


    #args = ("12")
    #result = db_worker.selectQuery(sql_templates.select_hw_by_id,args)

    #print("now: {0} || old: {1} || delta: {2} ".format(now,result[0][3],delta2))

    sys.exit(0)

def resetCounterIfDeltaOut(id, now):
    if deltaInSeconds > cfg.deltaTime or deltaInSeconds < 0:
        log.debug("reset counter, current deltaTime: {0}, cfg.deltaTime: {1}".format(deltaInSeconds, cfg.deltaTime))

        args = (1, now, id)
        if utils.isIp(id):
            state = db_worker.setQuery(sql_templates.update_by_ip, args)
        else:
            state = db_worker.setQuery(sql_templates.update_by_id, args)

    return state

def getHwFromDbOrInsertNew(id, now):
    selResult=""
    if utils.isIp(id):
        selResult = db_worker.selectQuery(sql_templates.select_hw_by_ip, id)
    else:
        selResult = db_worker.selectQuery(sql_templates.select_hw_by_id, id)

    if selResult == None:
        if utils.isIp(id):
            args = (None, id, "1", now)
            state = db_worker.setQuery(sql_templates.insert_new_hw, args)

            log.debug("insert new hw id {0} state: {1}".format(id, state))
        else:
            args = (id, None, "1", now)
            state = db_worker.setQuery(sql_templates.insert_new_hw, args)

            log.debug("insert new hw id {0} state: {1}".format(id, state))

    return selResult



def getHwData(ip_or_id):
    data = bugsapi.getData(ip_or_id)
    return data

def initLogging():
    log.basicConfig(filename=cfg.logFilePath,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
    #alose log to std out
    log.getLogger().addHandler(log.StreamHandler())


if __name__ == "__main__":
    main()
