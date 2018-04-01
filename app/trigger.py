import config as cfg
import sys
import os
import utils
import json
import db_worker
import sql_templates
import time
from datetime import datetime, timedelta
import logging as log
import log_parser
from pathlib import Path
from transliterate import translit


def main():
    initLogging()

    returnCode = db_worker.checkAndInitTable()
    if returnCode > 0:
        sys.exit(returnCode)

##
    now = datetime.now()
    minimumReqTime = datetime.now() - timedelta(seconds=cfg.deltaTime)

    log.debug("current time: {0}, minimum time: {1}, cfg delta: {2}".format(
        now, minimumReqTime, cfg.deltaTime))

    selResult = db_worker.selectQuery(sql_templates.select_hw_by_portdownDate, args=(
        minimumReqTime, cfg.minimumPortDownCount), all=True)

    hw_ids = []
    for line in selResult:
        id = line[0] if line[0] != None else line[1]
        hw_ids.append(id)

    # get hw data from bugs
    hwinfo = []
    for id in hw_ids:
        hwinfo.append(utils.getHwData(id))

    hw_to_triger = []
    hw_to_clean_only = []

    # filter by city white list
    for sw in hwinfo:
        if sw.city in cfg.cityWhiteList:
            hw_to_triger.append(sw)
        else:
            hw_to_clean_only.append(sw)

    # remove from trigger if notify disabled
    for sw in hw_to_triger:
        selResult = selectFromDBBySWObject(sw)

        if (selResult[5] < 1):
            hw_to_triger.remove(sw)
            hw_to_clean_only.append(sw)
            log.debug("remove hardware {0} with disable notifycation".format("d" + sw.id))

    # clean
    for sw in hw_to_clean_only:
        print(sw.ip)
        #auto get in method by match with query
        setDataBySw(sw,args=[0, None, None, None])

    #trigers and set db mark
    for info in hw_to_triger:
        print(prepareTransMsgForSMS(info))



    sys.exit(0)

def setDataBySw(sw, args):
    if db_worker.selectQuery(sql_templates.select_hw_by_id, "d" + sw.id) != None:
        args[3] = 'd' + sw.id
        db_worker.setQuery(sql_templates.update_to_trigger_by_id, args)
    else:
        args[3] = sw.ip
        db_worker.setQuery(sql_templates.update_to_trigger_by_ip, args)

def selectFromDBBySWObject(sw):
    selResult = db_worker.selectQuery(sql_templates.select_hw_by_ip, sw.ip)
    if selResult == None:
        selResult = db_worker.selectQuery(
            sql_templates.select_hw_by_id, "d" + sw.id)

    return selResult

def prepareTransMsgForSMS(info):
#   id | говрод | улица | дом | подъезд
    text = "{0} | {1} | {2} | {3} | {4}".format(
        info.id, info.city, info.street, info.home_number, info.home_entrance)
    return translit(text, "uk", reversed=True)



def initLogging():
    log.basicConfig(filename=cfg.logFilePath, format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=log.getLevelName(cfg.LogLevel))
    # alose log to std out
    log.getLogger().addHandler(log.StreamHandler())
    log.getLogger().setLevel(log.getLevelName(cfg.LogLevel))

if __name__ == "__main__":
    main()
