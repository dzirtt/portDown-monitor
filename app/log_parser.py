import config as cfg
import sys, bugsapi, utils
import logging as log

def main():
    initLogging()
    print(getHwData('d1115').ip)

    #get file, split by line, extract id\ip, upload to bd

    sys.exit(0)

def getHwData(ip_or_id):
    data = bugsapi.getData(ip_or_id)
    return data

def initLogging():
    log.basicConfig(filename=cfg.logFilePath,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=log.DEBUG)
    #alose log to std out
    log.getLogger().addHandler(log.StreamHandler())

if __name__ == "__main__":
    main()
