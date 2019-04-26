# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/1/23 11:24"
__all__ = ["__version__", "MangoDBHandle"]
__version__ = "1.0.0"
from ffm.db import Jzmongo
from ffm.config.jlog import JLogDecorator

from config import DB
from util import handle
import util


# database name
DL_DATABASE = "deadline10db"
FFM_DATABASE = "FFMDatabase"

# collection name
DL_USERINFO = "UserInfo"
DL_JOBS = "Jobs"
DL_CONFIG = "Configure"

FFM_USERINFO = "UserInfo"
FFM_CONFIG = "Configure"


BASE_INFO = {
            "_id": None,
            "Name": None,
            "Email" : "",
            "SendEmail" : False,
            "JobCompleted" : True,
            "JobFailed" : True,
            "JobWarning" : True,
            "JobTaskTimeout" : True,
            "Machine" : "",
            "SendPopup" : False,
            "SvcHash" : None,
            "Service" : "",
            "RunAsName" : "",
            "RunAsDom" : "",
            "RunAsHash" : "",
        # === Custom properties ===
            "Password": "",
            "CreateDate": None,
            "LastLoginTime": None,
            "LastLogoutTime": None,
            "TotalLoginTime": 0,
            "TotalRenderTime": 0,
            "EffectiveRenderTime": 0,
            "IP": "",
            "MyJobs": [],
            "TotalRenderCost": 0.00,
            "TotalPayed": 0.00,
            "UnitPrice": 0.00,  # 单价
            "TotalBalance": 0.00,  # 余额
            "RechargeRecord": [], # [{'Date': xxx, 'Money': xxx, ...}, {...}]
            "IsValid": True,
        }


class DBLog(JLogDecorator):
    pass


class MangoDBHandle(Jzmongo.mongoDB):
    def __init__(self):
        host = DB.FFM_DB_HOST
        port = DB.FFM_DB_PORT
        super(MangoDBHandle, self).__init__(host, port)

    def getCursor(self, database, collections):
        '''collection and table name, return cursor'''
        collection = self.connect(database, collections)
        return Jzmongo.mongoCursor(collection)

    @property
    def userCursor(self):
        return self.getCursor(DL_DATABASE, DL_USERINFO)

    @property
    def jobCursor(self):
        return self.getCursor(DL_DATABASE, DL_JOBS)

    @property
    def configCursor(self):
        return self.getCursor(DL_DATABASE, DL_CONFIG)

    def gerUsersName(self):
        return [x.values()[0] for x in self.userCursor.find({}, {"_id": 1})]

    def getUserInfo(self, name):
        info = self.userCursor.find_one({"_id": name}, {"_id": 0})
        if info:
            info.update({"_id": name})

        return info

    def getUsersInfo(self, name=None):
        if name:
            return self.getUserInfo(name)

        name_l = [x for x in self.userCursor.find({}, {})]
        res = []
        for n in name_l:
            r = self.getUserInfo(n["_id"])
            r.update(n)
            res.append(r)

        return res

    def saveUser(self, info):
        if not isinstance(info, dict):
            raise TypeError("saveUser info need dict type.")

        _id = info.get("_id")
        if not _id:
            return

        name = info.get("Name")
        if not name or name != _id:
            info.update({"Name": _id})

        i = BASE_INFO.copy()
        i.update(info)

        try:
            self._insertUser(**info)
        except Exception as e:
            self.userCursor.find_one_and_replace({"_id": _id}, i)

    def saveUserInfo(self, user, info):
        if not isinstance(info, dict):
            raise TypeError("saveUserInfo info need dict type.")
        self.userCursor.find_one_and_update({'_id': user}, {'$set': info})

    def updateUserInfo(self, username, key, value):
        if key not in ["TotalLoginTime", "TotalRenderTime", "EffectiveRenderTime", "TotalPayed", "TotalRenderCost"]:
            util.JLOG.warning("User %s attempt to change the value of (KEY: %s) is rejected, "
                              "(value: %s).\n\tReason: Key not useful." % (username, key, value))
            return
        self.userCursor.find_one_and_update({"_id": username}, {"$inc": {key: value}})

    def delUser(self, name):
        self.userCursor.delete_one({"_id": name})

    def _insertUser(self, **kwargs):
        info = BASE_INFO.copy()
        info.update(kwargs)
        if not info["_id"]:
            if not info["Name"]:
                return
            info["_id"] = info["Name"]

        if not info["CreateDate"]:
            info["CreateDate"] = handle.getUTCDate()

        self.userCursor.insert_one(info)

    def addJob2User(self, name, job_id):
        info = self.getUserInfo(name)
        if info:
            self.userCursor.update_one({"_id": name}, {"$addToSet": {"MyJobs": job_id}})

    def saveJobInfo(self, job_id, info):
        if not isinstance(info, dict):
            raise TypeError("saveJobInfo info need dict type.")
        self.jobCursor.find_one_and_update({'_id': job_id}, {'$set': info})

    def getJobInfo(self, job_id):
        info = self.jobCursor.find_one({"_id": job_id}, {"_id": 0})
        if info:
            info.update({"_id": job_id})

        # Manually check the mission status
        # If info["Stat"] == 1, and info["Props"]["Tasks"] == info["QueuedChunks"],
        # change info["Stat"] to 2, means job status is in Queue.
        if info["Stat"] == 1 and info["Props"]["Tasks"] == info["QueuedChunks"]:
            info["Stat"] = 2

        if info["Stat"] == 2 and info["Props"]["Tasks"] != info["QueuedChunks"]:
            info["Stat"] = 1

        return info

    def getJobReport(self, job_id):
        cursor = self.getCursor(DL_DATABASE, "JobReportEntries")

        info = cursor.find({"Job": job_id}, {"_id": 0})
        if info:
            # return {"Errors": [x for x in info]}
            return info

    def getConfigure(self):
        _id = [x for x in self.configCursor.find({}, {})]
        res = {}
        for n in _id:
            info = self.configCursor.find_one({"_id": n["_id"]}, {"_id": 0})
            if info:
                info.update({"_id": _id})
            info.update(n)
            res.update({n["_id"]: info})

        # {
        #   u'FTP': {u'FtpPath': u'\\\\192.168.1.47\\share\\Data\\FTP',
        #            '_id': u'FTP',
        #            u'FtpID': u'test1',
        #            u'FtpPwd': u'FFM@ftp!'
        #            },
        #   u'Software': {'_id': u'Software',
        #                 u'Max':
        #                     {u'Name': u'Max',
        #                      u'Versions': [u'2016', u'2017', u'2018', u'2019']
        #                     },
        #                 u'Maya':
        #                     {u'Name': u'Maya',
        #                      u'Versions': [u'2016', u'2017', u'2018']
        #                     }
        #              }
        #  }
        return res

    def initSaveConfigure(self, key):
        if key == "FTP":
            document = {"_id": key, u'FtpPath': "", u'FtpID': "", u'FtpPwd': ""}
        elif key == "Software":
            document = {'_id': u'Software'}
        else:
            return
        self.configCursor.insert_one(document)

    def saveConfigure(self, info):
        ftp_c = {"_id": "FTP"}
        soft_c = {"_id": "Software"}

        # {u'FTP': {u'FtpPath': u'\\\\192.168.1.47\\share\\Data\\FTP', '_id': u'FTP', u'FtpID': u'test1', u'FtpPwd': u'FFM@ftp!'}
        if info.get("FTP"):
            ftp_info = info["FTP"]
            ftp_c.update({
                "FtpPath": ftp_info.get("FtpPath"),
                "FtpID": ftp_info.get("FtpID"),
                "FtpPwd": ftp_info.get("FtpPwd"),
            })
            self.configCursor.find_one_and_replace({"_id": "FTP"}, ftp_c)

        # u'Software': {'_id': u'Software',
        #               u'Max': {u'Name': u'Max', u'Versions': [u'2016', u'2017', u'2018', u'2019']},
        #               u'Maya': {u'Name': u'Maya', u'Versions': [u'2016', u'2017', u'2018']}}}
        if info.get("Software"):
            soft_c.update(info["Software"])
            self.configCursor.find_one_and_replace({"_id": "Software"}, soft_c)

