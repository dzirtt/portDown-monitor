import smsApi, utils
import config as cfg
import telegramApi.telegramApi as telegaApi

class triggers:
    def action(text):
        pass
    def name():
        pass


class triggerSMS(triggers):
    def action(self, text):
        for phone in cfg.phoneList:
            status = smsApi.sendSms(phone, text)
            if not status:
                log.error("cant send sms to {0}".format(phone))

    def name(self):
        return "SMS"

class stdOutTrigger(triggers):
    def action(self, text):
        print(text)

    def name(self):
        return "std OUT"

class telegramTrigger(triggers):
    def action(self, text):
        telegaApi.sendMsg(text)

    def name(self):
        return "telegram"

    def __init__(self):
        telegaApi.initTelegramBot()
