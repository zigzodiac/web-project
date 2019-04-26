# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
loadLog: set util.JLOG.
date2str: datetime type transform to string.
str2date: string type transform to datetime.
formatTime: format time function, second to 00:00:00 format.
getLocalDate: pass in a date, return local date.
getUTCDate: pass in a date or not, return UTC date.
copy: copy file function, create dir auto.
unpackFiles: unzip file to current dir.
formatMoney: float number to money format (0.00 RMB)
showExplorer: show file in explorer and select it, or open dir in explorer.
checkDB: Call C# program loop check database content, real-time update data.
"""
__author__ = "jeremyjone"
__datetime__ = "2019/3/7 23:20"
__all__ = ["__version__", "loadLog", "date2str", "str2date", "formatTime",
           "getLocalDate", "getUTCDate", "copy", "unpackFiles", "formatMoney",
           "showExplorer", "checkDB"]
__version__ = "1.0.0"
import os
import datetime
import re
import zipfile
import subprocess
import json
import requests
from dateutil import parser
from ffm.config.jlog import JLog

from config import FILE, DB
from util.filecopy import copyFile
import util


def loadLog(level="INFO"):
    util.JLOG = JLog(FILE.FILE_LOG, level=level)


def copy(srcfile, dstfile):
    path = os.path.dirname(dstfile)
    if not os.path.exists(path):
        os.makedirs(path)

    copyFile(srcfile, dstfile)


def unpackFiles(_file):
    try:
        zf = zipfile.ZipFile(_file)
        zf.extractall(os.path.dirname(_file))
        zf.close()
    except:
        unpackFiles(_file)


def date2str(_date):
    try:
        return _date.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return _date.__str__()


def str2date(date):
    if isinstance(date, datetime.datetime):
        return date

    if isinstance(date, unicode):
        date = date.encode("utf-8")

    # if not isinstance(date, str):
    #     raise TypeError("str2date need str, you pass in %s" % type(date))

    fmt = '%Y-%m-%d %H:%M:%S'
    try:
        if re.findall(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", date):
            return datetime.datetime.strptime(date, fmt)
    except:
        pass
    return date.__str__()


def formatTime(time):
    if time and isinstance(time, float) or isinstance(time, int):
        h = int(time / 3600.0)
        m = int(time % 3600.0 / 60.0)
        s = int(time % 60.0)
        return "%02d:%02d:%02d" % (h, m, s)
    return "00:00:00"


def getLocalDate(date, timedelta=8):
    if isinstance(date, datetime.datetime):
        return date + datetime.timedelta(hours=timedelta)

    if isinstance(date, str) or isinstance(date, unicode):
        _date = parser.parse(date)
        return _date + datetime.timedelta(hours=timedelta)

    return datetime.datetime.now()


def getUTCDate(local_date=None, timedelta=8):
    try:
        if local_date:
            return local_date - datetime.timedelta(hours=timedelta)
        return datetime.datetime.now() - datetime.timedelta(hours=timedelta)
    except:
        return local_date.__str__()


def formatMoney(money):
    if money:
        if isinstance(money, float):
            return "{0:.2f} RMB".format(round(money, 2))
    return "{0:.2f} RMB".format(0)


def showExplorer(filename):
    try:
        if os.path.isfile(filename):
            subprocess.Popen(r'explorer /select,"%s"' % filename.replace('\\', os.sep))
        elif os.path.isdir(filename):
            os.startfile(filename)
        else:
            raise ValueError("%s is not correct, please check." % filename)
    except Exception as e:
        util.JLOG.warning("Server can not open '%s' in explorer, reason: %s" % (filename, e))


def sendFile2Slave(fileList, username, slaveList):
    for slave in slaveList:
        url = "http://%s:8080/api/files/copy" % slave
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data = {"Name": username, "Files": fileList}
        # print fileList
        r = requests.post(url, data=json.dumps(data), headers=headers)
        # print r


def checkDB(username, job_id):
    check_exe = os.path.join(os.path.dirname(__file__), os.path.pardir, "checkMongo", "MongoTest.exe")
    mongo_addr = "mongodb://localhost:27100"
    db_name = "deadline10db"
    coll_name = "Jobs"
    ip = DB.SERVER_HOST
    port = DB.SERVER_PORT
    interval_time = 2
    subprocess.Popen("%s %s %s %s %s %s %s %s %s" %
                     (check_exe, mongo_addr, db_name, coll_name, ip, port,
                      interval_time, username, job_id))
