# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/9 17:01"
__all__ = ["__version__", "ConfigModel"]
__version__ = "1.0.0"
import os, sys
from collections import OrderedDict
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore



class ConfigModel(QtGui.QStandardItemModel):
    HEAD_NAME = {
        "key": "App Name",
        "path": "App Check Path",
        "in": "Install Script",
        "un": "UnInstall Script",
    }

    def __init__(self, parent=None):
        super(ConfigModel, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.head = OrderedDict([("key", 0), ("path", 1), ("in", 2), ("un", 3)])
        self.setHorizontalHeaderLabels([self.HEAD_NAME[x] for x in self.head.keys()])

    def appendData(self, key, path, in_v, un_v):
        row = self.rowCount()
        self.insertRow(row)
        key_item = QtGui.QStandardItem(key)
        key_item.setToolTip(key)
        path_item = QtGui.QStandardItem(path)
        path_item.setToolTip(path)
        in_item = QtGui.QStandardItem(in_v)
        in_item.setToolTip(in_v)
        un_item = QtGui.QStandardItem(un_v)
        un_item.setToolTip(un_v)
        self.setItem(row, self.head["key"], key_item)
        self.setItem(row, self.head["in"], in_item)
        self.setItem(row, self.head["path"], path_item)
        self.setItem(row, self.head["un"], un_item)





# class PathModel(QtGui.QStandardItemModel):
#     HEAD_NAME = {
#         "key": "App Name",
#         "path": "App Check Path",
#     }
#
#     def __init__(self, parent=None):
#         super(PathModel, self).__init__(parent)
#         self.initUI()
#
#     def initUI(self):
#         self.head = OrderedDict([("key", 0), ("path", 1)])
#         self.setHorizontalHeaderLabels([self.HEAD_NAME[x] for x in self.head.keys()])
#
#     def appendData(self, key, path):
#         row = self.rowCount()
#         self.insertRow(row)
#         key_item = QtGui.QStandardItem(key)
#         path_item = QtGui.QStandardItem(path)
#         self.setItem(row, self.head["key"], key_item)
#         self.setItem(row, self.head["path"], path_item)

