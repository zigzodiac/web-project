# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/1/23 14:16"
__all__ = ["__version__", "ManageUserModel"]
__version__ = "1.0.0"

from collections import OrderedDict
import PySide.QtGui as QtGui

from util import handle


class ManageUserModel(QtGui.QStandardItemModel):
    HEAD = {
        "name": "Username",
        "pwd": "Password",
        "date": "Create Date",
        "price": "Price (Core/H)"
    }

    def __init__(self, parent=None):
        super(ManageUserModel, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.head = OrderedDict([("name", 0), ("pwd", 1), ("price", 2), ("date", 3)])

    def appendData(self, info_list):
        self.clear()
        self.setHorizontalHeaderLabels([self.HEAD[x] for x in self.head.keys()])

        for userClient in info_list.values():
            if userClient.isvalid == False:
                continue

            row = self.rowCount()
            self.insertRow(row)
            name_item = QtGui.QStandardItem(userClient.username)
            name_item.setToolTip(userClient.username)
            self.setItem(row, self.head["name"], name_item)

            pwd = userClient.password
            pwd_item = QtGui.QStandardItem(pwd)
            pwd_item.setToolTip(pwd)
            self.setItem(row, self.head["pwd"], pwd_item)

            price = str(userClient.unit_price)
            price_item = QtGui.QStandardItem(price)
            price_item.setToolTip(price)
            self.setItem(row, self.head["price"], price_item)

            c_date = userClient.create_time
            date_item = QtGui.QStandardItem(c_date)
            date_item.setToolTip(c_date)
            self.setItem(row, self.head["date"], date_item)





