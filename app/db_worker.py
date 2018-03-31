import config as cfg
import pymysql as mysql
import logging as log

def updateDb(hwid):
    pass

def testDBConnection():

    try:
        db = _openConnection()
        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")

        data = cursor.fetchone()
        cursor.close()
        db.close();
    except:
        return False

    return True


def tableIsExist(table):

    try:
        db = _openConnection()
        cursor = db.cursor()
        cursor.execute("""SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{0}'""".format(table.replace('\'', '\'\'')))
        data = cursor.fetchone()

        db.close()
        cursor.close()
    except:
        log.error("cant check table {0}".format(table))

    if data[0] == 1:
        return True

    return False


def _openConnection():
    try:
        db = mysql.connect(cfg.db['hostname'],cfg.db['user'],cfg.db['password'],cfg.db['dbName'] )
    except:
        log.error("cant connect to db with {0}".format(cfg.db))
        return None

    return db
