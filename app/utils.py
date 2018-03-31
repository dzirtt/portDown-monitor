import ipaddress

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
