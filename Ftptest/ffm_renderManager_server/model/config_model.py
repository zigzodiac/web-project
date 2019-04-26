# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/3/7 23:52"
__all__ = ["__version__", ]
__version__ = "1.0.0"
from database.db_handle import MangoDBHandle


class ConfigModel():
    def __init__(self):
        self.loadData()

    def loadData(self):
        md = MangoDBHandle()
        self.__info = md.getConfigure()
        md.disconnect()

        if not self.__info.get("FTP"):
            md.initSaveConfigure("FTP")
            md = MangoDBHandle()
            self.__info = md.getConfigure()
            md.disconnect()

        if not self.__info.get("Software"):
            md.initSaveConfigure("Software")
            md = MangoDBHandle()
            self.__info = md.getConfigure()
            md.disconnect()

        """
        {u'FTP': {u'FtpID': u'Administrator',
          u'FtpPath': u'\\\\192.168.1.47\\ftp',
          u'FtpPwd': u'FFM@ad!',
          '_id': u'FTP'},
         u'Software': {u'C4D': {u'Name': u'C4D',
                                u'Versions': [u'12',
                                              u'13',
                                              u'14',
                                              u'15',
                                              u'16',
                                              u'17',
                                              u'18',
                                              u'19']},
                       u'HOUDINI': {u'Name': u'HOUDINI',
                                    u'Versions': [u'14.0',
                                                  u'15.0',
                                                  u'15.5',
                                                  u'16.0',
                                                  u'16.5']},
                       u'MAX': {u'Name': u'MAX',
                                u'Versions': [u'2016', u'2017', u'2018', u'2019']},
                       u'MAYA': {u'Name': u'MAYA',
                                 u'Versions': [u'2016', u'2017', u'2018']},
                       u'NUKE': {u'Name': u'NUKE',
                                 u'Versions': [u'9.0',
                                               u'10.0',
                                               u'10.5',
                                               u'11.0',
                                               u'11.1',
                                               u'11.2']},
                       '_id': u'Software'}}
        """

        self.ftpID = self.__info["FTP"]["FtpID"]
        self.ftpPassword = self.__info["FTP"]["FtpPwd"]
        self.ftpPath = self.__info["FTP"]["FtpPath"]

        self.software = self.__info["Software"]

    def saveInfo(self):
        if not isinstance(self.software, dict):
            raise TypeError("Can not update configure database, "
                            "software information not dict type.")
        info = {u'FTP':
                    {u'FtpID': self.ftpID,
                     u'FtpPath': self.ftpPath,
                     u'FtpPwd': self.ftpPassword
                     },
                u'Software': self.software
                }

        md = MangoDBHandle()
        md.saveConfigure(info)
        md.disconnect()

    def getInfo(self):
        return self.ftpID, self.ftpPassword, self.ftpPath, self.software

    def getFTP(self):
        info = {
            'FtpPath': self.ftpPath,
            "FtpId": self.ftpID,
            "FtpPw": self.ftpPassword,
        }
        return info

    def getSoftwareVersion(self, soft):
        if self.software.get(soft):
            if self.software[soft].get("Versions"):
                return self.software[soft]["Versions"]
        return None
