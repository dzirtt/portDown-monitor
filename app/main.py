import config as cfg
import sys, os, utils, json
import db_worker
import sql_templates
import time
from datetime import datetime, timedelta
import logging as log
import log_parser
from pathlib import Path


def main():
    initLogging()

    # rsyslog file exist
    if not Path(cfg.rsyslogFilePath).is_file():
        log.error('file {0} not exist'.format(cfg.rsyslogFilePath))
        sys.exit(1)

    # check and init db tables
    returnCode = db_worker.checkAndInitTable()
    if returnCode > 0:
        sys.exit(returnCode)

    while True:
        now = datetime.now()
        hw_ids = log_parser.rsyslogFileWork(cfg.rsyslogFilePath)
        hw_ids_filtered = log_parser.filterPortDowns(hw_ids)
        for id,value in hw_ids_filtered.items():

            if value > cfg.maxPortDownPerOneScan:
                log.info("skip id {0} with value {1}".format(id,value))
                continue

            # add if not in tables
            result = getHwFromDbOrInsertNew(id, now, value)
            if result == None:
                continue

            try:
                updateCounter(id, now, result, value)
            except:
                log.info("cant get info from db {0}".format(result))
                continue

        procTime=(datetime.now() - now).total_seconds()
        log.debug("{0} lines : check by {1} seconds".format(len(hw_ids_filtered),procTime))

        #delay process
        startDelayTime = datetime.now()
        delta = 0

        while delta < cfg.rotateDelay:
            delta = (datetime.now() - startDelayTime).total_seconds()
            time.sleep(0.5)



    sys.exit(0)

def _test():
    hw_ids = log_parser.rsyslogFileWork(cfg.rsyslogFilePath)
    hw_ids_filtered = log_parser.filterPortDowns(hw_ids)
    for id, count in hw_ids_filtered.items():
        print("{0}:{1}".format(id,count))
    #print(json.dumps(hw_ids_filtered, indent=2))

    #args = ("12")
    #result = db_worker.selectQuery(sql_templates.select_hw_by_id,args)

    #print("now: {0} || old: {1} || delta: {2} ".format(now,result[0][3],delta2))


def updateCounter(id, now, result, value):
    currentCounter = result[2]
    # first port down date
    portDownDate = result[3]
    deltaInSeconds = (now - portDownDate).total_seconds()

    # delta < 0 its may be error in app. or wrong date on server betwen app
    # starts
    if deltaInSeconds > cfg.deltaTime or deltaInSeconds < -1:
        args = (value, now, id)
        log.debug("reset counter, current deltaTime:{0}, cfg.deltaTime:{1}".format(
            deltaInSeconds, cfg.deltaTime))
    else:
        # increment counter
        newCounter = currentCounter + value
        args = (newCounter, portDownDate, id)
        log.debug("update port counter on hw:{0} counter:{1}".format(id, newCounter))

    # update counter
    if utils.isIp(id):
        state = db_worker.setQuery(sql_templates.update_by_ip, args)
    else:
        state = db_worker.setQuery(sql_templates.update_by_id, args)

    log.debug("Changes commit state: {0}".format(state))

    return True

def getHwFromDbOrInsertNew(id, now, value):
    selResult = ""
    if utils.isIp(id):
        selResult = db_worker.selectQuery(sql_templates.select_hw_by_ip, id)
    else:
        selResult = db_worker.selectQuery(sql_templates.select_hw_by_id, id)

    if selResult == None:
        if utils.isIp(id):
            args = (None, id, value, now)
            state = db_worker.setQuery(sql_templates.insert_new_hw, args)

            log.debug("insert new hw id {0} state: {1}".format(id, state))
        else:
            args = (id, None, value, now)
            state = db_worker.setQuery(sql_templates.insert_new_hw, args)

            log.debug("insert new hw id {0} state: {1}".format(id, state))

    return selResult

def initLogging():
    log.basicConfig(filename=cfg.logFilePath, format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S', level=log.getLevelName(cfg.LogLevel))
    # alose log to std out
    log.getLogger().addHandler(log.StreamHandler())
    log.getLogger().setLevel(log.getLevelName(cfg.LogLevel))

def test():
    hwLogs = log_parser.parseFile(cfg.rsyslogFilePath)
    hwIdsOnly = []

    for line in hwLogs:
        try:
            hw = line.split(' ')[3]
            if not utils.isIpOrId(hw):
                 hw = line.split(' ')[4]
            
            if(utils.isIpOrId(hw)):
                hwIdsOnly.append(hw)
                
            print(hw)
                
        except:
            raise
            log.warning('cant parse line "{0}"'.format(line))
    
if __name__ == "__main__":
    main()
