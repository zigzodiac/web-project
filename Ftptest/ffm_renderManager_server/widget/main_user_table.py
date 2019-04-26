# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
User table
"""
__author__ = "jeremyjone"
__datetime__ = "2019/3/4 16:34"
__all__ = ["__version__", "UserTable"]
__version__ = "1.0.0"

import os, sys
from collections import OrderedDict
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from util import handle
from widget.job_widget import JobWidget
import connect


class UserTable(QtGui.QTableWidget):
    HEAD = OrderedDict([
        ("Name", 0),
        ("IP", 1),
        ("Price", 2),
        ("Balance", 3),
        ("RootPath", 4),
        ("TotalRenderTime", 5),
        ("JobCount", 6),
        ("TotalCost", 7),
        ("LastLoginTime", 8),
        ("LastLogoutTime", 9),
        ("TotalLoginTime", 10),
    ])

    def __init__(self, parent=None):
        super(UserTable, self).__init__(parent)
        self.setColumnCount(len(self.HEAD))
        self.setHorizontalHeaderLabels(self.HEAD.keys())
        self.verticalHeader().hide()
        self.setEditTriggers(self.NoEditTriggers)  # edit disable
        self.setSelectionBehavior(self.SelectRows)  # row select mode
        self.setColumnWidth(self.HEAD["Name"], 100)
        self.setColumnWidth(self.HEAD["RootPath"], 200)
        self.setColumnWidth(self.HEAD["LastLoginTime"], 150)
        self.setColumnWidth(self.HEAD["LastLogoutTime"], 150)
        self.setColumnWidth(self.HEAD["TotalLoginTime"], 150)
        self.setColumnWidth(self.HEAD["TotalRenderTime"], 150)
        self.setColumnWidth(self.HEAD["Price"], 70)
        self.setColumnWidth(self.HEAD["JobCount"], 80)

        self.cellDoubleClicked.connect(self.doubleClickHandle)

    def insertUser(self, userClient):
        row = self.rowCount()
        self.insertRow(row)

        # insert user name, QTableWidgetItem can be sort, find..., QLabel can not.
        userItem = QtGui.QTableWidgetItem(userClient.username)
        self.setItem(row, self.HEAD["Name"], userItem)

        ipItem = QtGui.QTableWidgetItem(userClient.ip)
        self.setItem(row, self.HEAD["IP"], ipItem)

        rootPathItem = QtGui.QTableWidgetItem(userClient.root_path)
        self.setItem(row, self.HEAD["RootPath"], rootPathItem)

        lastLoginTimeItem = QtGui.QTableWidgetItem(userClient.last_login_time)
        self.setItem(row, self.HEAD["LastLoginTime"], lastLoginTimeItem)

        lastLogoutTimeItem = QtGui.QTableWidgetItem(userClient.last_logout_time)
        self.setItem(row, self.HEAD["LastLogoutTime"], lastLogoutTimeItem)

        totalLoginTimeItem = QtGui.QTableWidgetItem(handle.formatTime(userClient.total_login_time))
        self.setItem(row, self.HEAD["TotalLoginTime"], totalLoginTimeItem)

        jobCountItem = QtGui.QTableWidgetItem(len(userClient.jobs).__str__())
        self.setItem(row, self.HEAD["JobCount"], jobCountItem)

        totalRenderTimeItem = QtGui.QTableWidgetItem(handle.formatTime(userClient.total_render_time))
        self.setItem(row, self.HEAD["TotalRenderTime"], totalRenderTimeItem)

        priceItem = QtGui.QTableWidgetItem(handle.formatMoney(userClient.unit_price))
        self.setItem(row, self.HEAD["Price"], priceItem)

        totalPayedItem = QtGui.QTableWidgetItem(handle.formatMoney(userClient.total_payed))
        self.setItem(row, self.HEAD["TotalCost"], totalPayedItem)

        balanceItem = QtGui.QTableWidgetItem(handle.formatMoney(userClient.total_balance))
        self.setItem(row, self.HEAD["Balance"], balanceItem)

        # sort user list by name
        self.sortItems(self.HEAD["Name"])

    def getItem(self, name):
        '''get table item by name, if not item, return none'''
        item = self.findItems(name, QtCore.Qt.MatchFixedString)
        if item:
            return item[0]
        return None

    @property
    def selectRow(self):
        sel_item = self.selectedItems()
        if sel_item:
            return sel_item[0].row()
        return -1


    def updateInfo(self, userClient):
        '''update user table information'''
        item = self.getItem(userClient.username)
        if not item:
            return

        # remove row and insert new row.
        self.removeRow(item.row())
        self.insertUser(userClient)

    def doubleClickHandle(self, row, column):
        username = self.item(row, self.HEAD["Name"]).text()
        user_client = connect.clients.get_rc(username)
        if user_client.job_window == None:
            user_client.job_window = JobWidget(username)
        user_client.job_window.show()
