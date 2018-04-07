import config as cfg
import urllib
import ssl, json, utils
import logging as log

def sendSms(phone, text):
    try:
        data = {}

        data["phone"] = phone
        data["text"] = utils.prepareTransMsgForSMS(text)

        dataBytes = bytes(urllib.parse.urlencode( data ).encode())
        responce = urllib.request.urlopen(cfg.smsGateApiURL, dataBytes);

        responceText = responce.read().decode('utf-8')

        if 'complete' in responceText:
            log.info("send sms to {0}".format(phone))
            return True

        log.info("send sms to {0}".format(phone))
    except:
        log.error("cant send sms to {0}".format(phone))
        return False

    return False
