import ipaddress, bugsapi
from transliterate import translit

def isIp(ip):
    try:
        a=ipaddress.ip_address(ip)
    except:
        return False
    return True

def isIpOrId(ip_or_id):
    if( isIp(ip_or_id.strip()) or ip_or_id[0] == 'd'):
            return True

    return False

def getHwData(ip_or_id):
    data = bugsapi.getData(ip_or_id)
    return data

def prepareTransMsgForSMS(info):
#   id | говрод | улица | дом | подъезд
    return translit(text, "uk", reversed=True)
