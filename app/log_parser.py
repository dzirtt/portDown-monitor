import logging as log

def parseAndCleanFile(logFilePath):
    lines  = _parseFile(logFilePath)
    #_clearFile(logFilePath)

    return lines


def _parseFile(logFilePath):
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
