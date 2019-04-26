# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/2/15 14:39"
__all__ = ["__version__", "CopyHandle"]
__version__ = "1.0.0"
import sys, os
import time
from ffm.file.jfile import MD5File

from util.handle import copy, unpackFiles, sendFile2Slave
import util
from connect import protocol
from connect.deadline_connect import DLConnect
import connect

reload(sys)
sys.setdefaultencoding("utf8")


class MyFile():
    def __init__(self, hash, ftp_path, local_path):
        self.hash = hash
        self.ftp_path = ftp_path
        self.local_path = local_path


class CopyHandle():
    def __init__(self, data):
        self._data = data
        self.username = data[u"JobInfo"][u"UserName"]
        self._file_size = -1
        self._check_interval = 3

        self._file_list = []
        self.zip_file_list = []
        self.bad_file_list = []
        self.run_flag = True
        self.createFileObj()

    def createFileObj(self):
        # FileInfo, [{'zip': 'zip filename', 'file': ['filename1', 'filename2', ...]},
        #            {"Local": path, "Ftp": path}, {...}]
        zipfile = self._data[u"FileInfo"][0]
        self.zip_file_list = zipfile[u'file']
        try:
            unpackFiles(zipfile[u'zip'])  # unpack zip file
        except:
            connect.sendMessageByName(self.username,
                                      protocol.MessageType.submit_result_from_server,
                                      {u'Result': u'Failed', u'ErrorFile': [zipfile[u'zip'], ]}
                                      )
            self.run_flag = False
            return

        for _file in self._data[u"FileInfo"][1:]:
        # for _file in self._data["FileInfo"]:
            ftp_path = _file[u"Ftp"][0]  # 0 is file path
            hash = _file[u"Ftp"][1]  # 1 is file hash value
            local_path = _file[u"Local"]
            # unzip zip file, get file which need copy to server disk.
            if local_path in zipfile[u'file']:
                self._file_list.append(MyFile(hash, ftp_path, local_path))

    def _check(self, _file):
        # print _file.ftp_path, _file.hash
        while os.path.getsize(_file.ftp_path) != self._file_size:  # not same, to be system writing...
            self._file_size = os.path.getsize(_file.ftp_path)
            time.sleep(self._check_interval)  # wait few second for system ftp write file.

        file_hash = MD5File(_file.ftp_path)
        if file_hash != _file.hash:
            # print "=========== BAD FILE =============="
            # print _file.hash
            # print file_hash
            util.JLOG.error("BAD File, %s" % _file.ftp_path)
            self.bad_file_list.append(_file.local_path)

    def checkHandle(self):
        for my_file in self._file_list:
            self._check(my_file)

        _ok_flag = False
        if len(self.bad_file_list):
            res = {u'Result': u'Failed', u'ErrorFile': self.bad_file_list}
        else:
            res = {u'Result': u'Success'}
            _ok_flag = True
        connect.sendMessageByName(self.username,
                                  protocol.MessageType.submit_result_from_server,
                                  res
                                  )

        # if not bad file, upload file success, can copy file and render.
        if _ok_flag:
            self.copyHandle()

    def copyHandle(self):
        dl = DLConnect()
        slaveList = dl.getSlaveInfo(self.username, "IP")
        # util.JLOG.printInfo("slave list: ", slaveList, self._file_list)

        _file_list = []
        for _file in self._file_list:
            ftp_path = _file.ftp_path
            local_path = _file.local_path

            if local_path.startswith("C:"):
                _file_list.append({"Ftp": ftp_path, "Local": local_path})
            else:
                copy(ftp_path, local_path)

        sendFile2Slave(_file_list, self.username, slaveList)

        user_client = connect.clients.get_rc(self.username)
        user_client.submitHandle(self._data)

