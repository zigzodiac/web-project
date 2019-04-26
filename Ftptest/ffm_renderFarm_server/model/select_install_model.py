# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/9 18:33"
__all__ = ["__version__", "SelectInstallModel"]
__version__ = "1.0.0"

import os, sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore


class SelectInstallModel(QtGui.QStandardItemModel):
    def __init__(self, parent=None):
        super(SelectInstallModel, self).__init__(parent)
        self.itemChanged.connect(self.listSelectChangeHandle)

    def appendData(self, key):
        row = self.rowCount()
        self.insertRow(row)
        item = QtGui.QStandardItem(key)
        item.setCheckable(True)
        self.setItem(row, item)

    def listSelectChangeHandle(self, item):
        # print "listSelectChangeHandle"
        for i in self.getAllItems:
            if i.checkState() == QtCore.Qt.Unchecked:
                self.parent().select_box.setCheckState(QtCore.Qt.Unchecked)
                return

        self.parent().select_box.setCheckState(QtCore.Qt.Checked)

    @property
    def getAllItems(self):
        row = self.rowCount()
        l = []
        for i in range(row):
            l.append(self.item(i))
        return l
