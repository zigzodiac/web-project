# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/22 18:16"
__all__ = ["__version__", "ManageUserDg", ]
__version__ = "1.0.0"

import os, sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from widget.edit_user_dialog import EditUserDg
from config import FILE, PARAM
from connect.deadline_connect import DLConnect
from database.db_handle import MangoDBHandle
from model.manage_user_model import ManageUserModel
from model.client_model import RenderClient
from util import handle
import util
import widget


class ManageUserDg(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ManageUserDg, self).__init__(parent)
        self.initUI()

        self.md = MangoDBHandle()

        self.user_model = ManageUserModel()
        self.user_table.setModel(self.user_model)

        self.loadData()

    def initUI(self):
        ui_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.UI_MANAGE_USER)
        css_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.CSS_MAIN)
        win = widget.UILoader(ui_file, css_file)

        l = win.findChild(QtGui.QLayout, "verticalLayout")
        self.setLayout(l)
        self.resize(win.width(), win.height())
        self.setWindowTitle("Manage User Dialog")
        self.setStyleSheet(win.styleSheet())

        newBtn = self.findChild(QtGui.QPushButton, "newUser")
        newBtn.clicked.connect(self.newUserHandle)
        editBtn = self.findChild(QtGui.QPushButton, "editUser")
        editBtn.clicked.connect(self.editUserHandle)
        delBtn = self.findChild(QtGui.QPushButton, "delUser")
        delBtn.clicked.connect(self.delUserHandle)
        addUserPoolBtn = self.findChild(QtGui.QPushButton, "addUserPoolBtn")
        addUserPoolBtn.clicked.connect(self.addUserPoolHandle)
        closeBtn = self.findChild(QtGui.QPushButton, "closeBtn")
        closeBtn.clicked.connect(self.close)
        saveAllBtn = self.findChild(QtGui.QPushButton, "saveAllBtn")
        saveAllBtn.clicked.connect(self.saveAllHandle)

        self.user_table = self.findChild(QtGui.QTableView, "tableView")
        self.user_table.doubleClicked.connect(self.doubleClickTable)

    def loadData(self):
        _info_list = self.md.getUsersInfo()
        self.user_info = {x["Name"]: RenderClient(x["Name"], isOnline=False) for x in _info_list if x["Name"].lower() not in PARAM.ADMIN_LIST}

        self.user_model.appendData(self.user_info)
        self.user_table.setColumnWidth(self.user_model.head["name"], 150)
        self.user_table.setColumnWidth(self.user_model.head["pwd"], 200)
        self.user_table.setColumnWidth(self.user_model.head["price"], 100)
        self.user_table.setColumnWidth(self.user_model.head["date"], 250)
        self.user_table.sortByColumn(self.user_model.head["name"], QtCore.Qt.AscendingOrder)

    def newUserHandle(self):
        # print "newUserHandle"
        editUserDg = EditUserDg(parent=self)
        while editUserDg.exec_():
            new_name = editUserDg.userText
            # name is null
            if not new_name:
                continue

            # name is exist
            if new_name in self.user_info.keys():
                message = "You are creating <b>%s</b> user, this name already exists." % new_name
                QtGui.QMessageBox.warning(self, "Name Error", message)
                continue

            # name break the rule.
            if new_name.lower() in PARAM.ADMIN_LIST:
                message = "User name could not contains the following:<br><b>%s</b>" % ", ".join(PARAM.ADMIN_LIST)
                QtGui.QMessageBox.warning(self, "Name Error", message)
                continue

            editUserDg.save()

            # Create User pool
            self.__createUserPool(new_name)

            self.loadData()
            break

    def doubleClickTable(self, model):
        # print model
        self.editUserHandle(model)

    def editUserHandle(self, index=None):
        # print "editUserHandle"
        if not index:
            if not self.selectItem:
                return
            row  = self.selectItem.row()
        else:
            row = index.row()

        name = self.user_model.data(self.user_model.index(row, self.user_model.head["name"]))

        user = self.user_info[name]

        editUserDg = EditUserDg(user=user, parent=self)
        if editUserDg.exec_():
            editUserDg.save()
            self.loadData()

    def delUserHandle(self):
        # print "delUserHandle"
        if not self.selectItem:
            return
        name = self.user_model.data(self.selectItem)

        reply = QtGui.QMessageBox.question(self, "Delete Warning",
                                          "Are you sure want to delete user <b>%s</b>? <br>Notice: It cannot be restored after deletion." % name,
                                          QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                          QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            # Delete user
            self.md.delUser(name)

            # Delete user pool
            dl = DLConnect()
            dl.deadlineCon.Pools.DeletePool(name)

            self.loadData()

    def saveAllHandle(self):
        for rc in self.user_info.values():
            rc.saveInfo()

        self.close()

    def addUserPoolHandle(self):
        if not self.selectItem:
            return

        name = self.user_model.data(self.selectItem)
        if self.__createUserPool(name):
            timer = QtCore.QTimer()
            msgBox = QtGui.QMessageBox(self)
            msgBox.setWindowTitle("Create Success!")
            msgBox.setText("<b>%s</b> Pool is created!" % name)
            timer.singleShot(1500, msgBox, QtCore.SLOT("close()"))
            msgBox.exec_()

    @property
    def selectItem(self):
        index = self.user_table.selectedIndexes()
        if index:
            return index[0]

    def __createUserPool(self, name):
        dl = DLConnect()
        res = dl.deadlineCon.Pools.AddPool(name)
        if res != "Success":
            util.JLOG.error("Create Deadline Pool, username: %s, information: %s" % (name, res))
            QtGui.QMessageBox.warning(self, "Create Deadline Pool Error!",
                                      "Username: <b>%s</b><br>Information: %s"
                                      "<br><br>You can manage by manual." % (name, res)
                                      )
            return False
        return True

