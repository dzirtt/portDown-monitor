import logging as log
import utils

def rsyslogFileWork(logFilePath):
    hwLogs = parseAndCleanFile(logFilePath)
    hwIdsOnly = []

    for line in hwLogs:
        try:
            hw = line.split(' ')[3]
            if(utils.isIpOrId(hw)):
                hwIdsOnly.append(hw)
        except:
            log.warning('cant parse line "{0}"'.format(line))

    return hwIdsOnly

def parseAndCleanFile(logFilePath):
    lines  = _readFile(logFilePath)
    #_clearFile(logFilePath)

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
