import config as cfg
import pymysql as mysql
import logging as log
import sql_templates

def createTable(template):
    try:
        db = _openConnection()
        cursor = db.cursor()
        cursor.execute(template)

        db.commit()
        cursor.close()
        db.close()
    except:
        log.error("cant create table from template {0}".format(template))
        return False

    return True

def initNewHardwareTables():
    db = _openConnection()
    cursor = db.cursor()

    cursor.execute(sql_templates.drop_hardware_table)

    db.commit()
    db.close()

    createTable(sql_templates.create_hardware_table)

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

def _testQuery(template,args):
    try:
        db = _openConnection()
        cursor = db.cursor()
        cursor.execute(template,args)

        db.commit()

        cursor.close()
        db.close()
    except:
        log.error("cant create table from template {0}".format(template))
        return False

    return True

def setQuery(template,args):
    try:
        db = _openConnection()
        cursor = db.cursor()
        cursor.execute(template,args)

        db.commit()

        cursor.close()
        db.close()
    except:
        raise
        log.error("cant add update db from template {0}".format(template))
        return False

    return True

def selectQuery(template,args,all=False):
    try:
        db = _openConnection()
        cursor = db.cursor()
        cursor.execute(template,args)

        if all:
            data = cursor.fetchall()
        else:
            data = cursor.fetchone()

        cursor.close()
        db.close()
    except:
        log.error("cant select from table with template {0}".format(template))
        return None

    return data

def _openConnection():
    try:
        db = mysql.connect(cfg.db['hostname'],cfg.db['user'],cfg.db['password'],cfg.db['dbName'] )
    except:
        log.error("cant connect to db with {0}".format(cfg.db))
        return None

    return db

def checkAndInitTable():
    if testDBConnection():
        if not tableIsExist(cfg.db["hwTable"]):
            if not createTable(sql_templates.create_hardware_table):
                log.error("cant create new hardware table from template '{0}''".format('create_hardware_table'))
                return 2
            else:
                log.info("create new table hardware from template '{0}''".format('create_hardware_table'))
    else:
        log.error("cant connect to db with {0}".format(cfg.db))
        return 2

    return 0
