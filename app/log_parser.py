import logging as log
import utils
from collections import Counter

def rsyslogFileWork(logFilePath):
    hwLogs = parseFile(logFilePath)
    _clearFile(logFilePath)
    hwIdsOnly = []

    for line in hwLogs:
        try:
            hw = line.split(' ')[3]
            if(utils.isIpOrId(hw)):
                hwIdsOnly.append(hw)

        except:
            log.warning('cant parse line "{0}"'.format(line))

    return hwIdsOnly

def filterPortDowns(hwids):
    return dict(Counter(hwids))


def parseFile(logFilePath):
    lines  = _readFile(logFilePath)

    return lines


def _readFile(logFilePath):
    f = open(logFilePath, "r")
    lines = f.readlines()
    f.close()
    return lines


def _clearFile(logFilePath):
    f = open(logFilePath, "w")
    f.seek(0)
    f.truncate()
    f.close
    log.debug("clear file {0}".format(logFilePath))
