import ipaddress

def isIp(ip):
    try:
        a=ipaddress.ip_address(ip)
    except:
        return False
    return True
