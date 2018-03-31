import config as cfg
import urllib.request as req
import ssl, json, utils
import logging as log

__ctx = ssl.create_default_context()
__ctx.check_hostname = False
__ctx.verify_mode = ssl.CERT_NONE

#id d1230

def getData(ip_or_id):
    if(utils.isIp(ip_or_id.strip())):
        apiurl=cfg.bugsApiURL + 'ip=' + ip_or_id
    else:
        if( ip_or_id[0] == 'd' ):
            apiurl=cfg.bugsApiURL + 'id=' + ip_or_id[1:]
        else:
            return None

    log.debug(apiurl)

    try:
        responce = req.urlopen(apiurl, context=__ctx)
        jsonData = json.loads(responce.read().decode('utf-8'))

        hwDataInst = hwData()
        hwDataInst.id = jsonData[0][0]
        hwDataInst.ip = jsonData[0][1]
        hwDataInst.city = jsonData[0][2]
        hwDataInst.street = jsonData[0][3]
        hwDataInst.home_number = jsonData[0][4]
        hwDataInst.home_entrance = jsonData[0][5]
    except:
        return None

    return hwDataInst


def getByip(ip):
    apiurl=cfg.bugsApiURL + 'ip=' + ip
    responce = req.urlopen(apiurl, context=__ctx)

    log.debug(apiurl)
    jsonData = json.loads(responce.read().decode('utf-8'))

    hwDataInst = hwData()
    hwDataInst.id = jsonData[0][0]
    hwDataInst.ip = jsonData[0][1]
    hwDataInst.city = jsonData[0][2]
    hwDataInst.street = jsonData[0][3]
    hwDataInst.home_number = jsonData[0][4]
    hwDataInst.home_entrance = jsonData[0][5]

    return hwDataInst

def getByid(id):
    apiurl=cfg.bugsApiURL + 'id=' + id
    responce = req.urlopen(apiurl, context=__ctx)

    log.debug(apiurl)
    return json.loads(responce.read().decode('utf-8'))

class hwData(object):
    id=0
    ip=""
    city=""
    street=""
    home_number=""
    home_entrance=""

    def __init__(self):
        pass
