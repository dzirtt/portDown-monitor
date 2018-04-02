import smsApi, utils
import config as cfg

class triggers:
    def action(text):
        pass


class triggerSMS(triggers):
    def action(self, text):
        for phone in cfg.phoneList:
            status = smsApi.sendSms(phone, text)
            if not status:
                log.error("cant send sms to {0}".format(phone))

class stdOutTrigger(triggers):
    def action(self, text):
        print(text.encode("utf-8"))
