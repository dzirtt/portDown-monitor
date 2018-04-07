import telegram
import sys
import json
import logging as log
import config as cfg


def test():
    initTelegramBot()

    status = ''
    try:

        if botIsLive():
            print("bot alive")

        status = sendMsg("Robo world is HELL")

    except:
        log.error("can't send message to {0}".format(cfg.telegramGroupId))

    print(status)
    # print(bot.get_me())

    sys.exit(0)

def sendMsg(msg):

    status = ""
    try:
        status = bot.sendMessage(chat_id=cfg.telegramGroupId, text=msg)
    except:
        log.error("can't send telegram message")
        raise

    if status != None:
        log.debug("message telegram send")
        return True

    return False


def initTelegramBot():
    global bot
    bot = telegram.Bot(cfg.telegramToken)


def botIsLive():
    status = False
    try:
        getMe = bot.get_me()
        status = True
    except:
        pass

    return status


if __name__ == "__main__":
    test()
