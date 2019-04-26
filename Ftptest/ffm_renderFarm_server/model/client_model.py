# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/2 16:25"
__all__ = ["__version__", "JClientModel"]
__version__ = "1.0.0"

import os, sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
from collections import OrderedDict

from config import PARAM



class JClientModel(QtGui.QStandardItemModel):

    HEAD_NAME = {
        "name": "Machine Name",
        "ip": "Machine IP",
        "app": "Installed Apps",
    }


    def __init__(self, parent=None):
        super(JClientModel, self).__init__(parent)
        self.__data = dict()
        self.initUI()

    def initUI(self):
        self.head = OrderedDict([("name", 0), ("ip", 1), ("app", 2)])
        self.setHorizontalHeaderLabels([self.HEAD_NAME[x] for x in self.head.keys()])

    @property
    def data(self):
        # {pc_name: info}
        return self.__data

    def appendData(self, data):
        # print "append data", data

        pc_name = data[PARAM.NAME]
        self.data.update({pc_name: data})

        root_item = self.invisibleRootItem()

        pc_item = QtGui.QStandardItem(pc_name)
        root_item.appendRow(pc_item)
        pc_item.setCheckable(True)

        # ip_item = QtGui.QStandardItem(data[PARAM.IP])
        # pc_item.appendColumn(ip_item)

        # app_item = QtGui.QStandardItem(", ".join([str(x) for x in data[PARAM.APPS]]))
        # pc_item.appendColumn(data[PARAM.APPS])

        # for apps in data[PARAM.APPS]:
        #     if nodeType is None:
        #         item.setCheckable(True)
        #         item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        #         item.setCheckState(QtCore.Qt.Unchecked)
        #     if userlist and user.get("username") in userlist:
        #         item.setCheckState(QtCore.Qt.Checked)
        #     dep_item.appendRow(item)

    def removeData(self, data):
        # print "remove data", data

        if self.data[data[PARAM.NAME]][PARAM.IP] == data[PARAM.IP]:
            del self.data[data[PARAM.NAME]]


