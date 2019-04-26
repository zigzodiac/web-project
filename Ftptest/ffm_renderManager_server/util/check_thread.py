# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/3/14 16:35"
__all__ = ["__version__", ]
__version__ = "1.0.0"
import os
import sys
import threading
from ffm.file.jfile import MD5File

import connect
from connect import protocol


class CheckFileMD5(threading.Thread):
    def __init__(self, data):
        super(CheckFileMD5, self).__init__()
        self.invalid_list = []
        self.repeat_list = []
        self.res = {'Result': 'Success', "Repeat": self.repeat_list}
        self.data = data
        self.username = data['UserName']

    def run(self):
        # self.data: [{zip...}, {"Local": path_str, "Ftp": (ftp_str, md5_str)}, {"Local": ..., "Ftp": ...}]
        for _file in self.data["FileInfo"][1:]:
            if os.path.exists(_file["Local"]):
                # If upload file is exist on server disk,
                # add to repeat_list and send to client,
                # client will not upload this file again.
                # Check method: use MD5.
                #
                # When file name as same as server disk,
                # and MD5 not same, return invalid to client.
                if _file["Ftp"][1] == MD5File(_file["Local"]):
                    self.repeat_list.append(_file["Local"])
                else:
                    self.invalid_list.append(_file["Local"])

        if self.invalid_list:
            self.res = {'Result': 'Failed', 'Errors': self.invalid_list}

        connect.sendMessageByName(self.username,
                                  protocol.MessageType.get_file_valid_from_server,
                                  self.res)
