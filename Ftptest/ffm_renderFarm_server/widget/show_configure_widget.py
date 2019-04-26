# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/9 12:22"
__all__ = ["__version__", ]
__version__ = "1.0.0"

import os, sys, datetime
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from widget.ui_load import UILoader
from config import FILE
from util import handle
import util
from model.config_command import Command
from model.config_tree_model import ConfigModel
from widget.change_configure_widget import ChangeConfiglDg



class JEditBase(QtGui.QDialog):
    def __init__(self, parent=None):
        super(JEditBase, self).__init__(parent)

        win = UILoader(os.path.join(os.path.dirname(__file__), os.pardir, FILE.UI_EDIT_CONFIG),
                       os.path.join(os.path.dirname(__file__), os.pardir, FILE.CSS_MAIN))

        self.table_widget = win.findChild(QtGui.QTableView, "tableView")

        new_btn = win.findChild(QtGui.QPushButton, "newBtn")
        new_btn.clicked.connect(self.newConfigHandle)

        edit_btn = win.findChild(QtGui.QPushButton, "editBtn")
        edit_btn.clicked.connect(self.editConfigHandle)

        del_btn = win.findChild(QtGui.QPushButton, "delBtn")
        del_btn.clicked.connect(self.delConfigHandle)

        backup_btn = win.findChild(QtGui.QPushButton, "backupBtn")
        backup_btn.clicked.connect(self.backupConfigHandle)

        btn_box = win.findChild(QtGui.QDialogButtonBox, "buttonBox")
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

        l = win.findChild(QtGui.QLayout, "formLayout")
        self.setLayout(l)

    def addValue(self):
        pass

    def getListValue(self):
        pass

    def newConfigHandle(self):
        i = QtGui.QStandardItem()
        self.table_model.insertRow(self.table_model.rowCount(), i)

    def delConfigHandle(self):
        if self.selectItem:
            self.table_model.removeRow(self.selectItem.row())

    def editConfigHandle(self):
        pass

    def backupConfigHandle(self):
        pass

    @property
    def selectItem(self):
        index = self.table_widget.selectedIndexes()
        if index:
            return index[0]






class JEditConfigWidget(JEditBase):
    def __init__(self, parent=None):
        super(JEditConfigWidget, self).__init__(parent)

        self.table_model = ConfigModel()
        self.table_widget.setModel(self.table_model)
        self.table_widget.setColumnWidth(self.table_model.head["key"], 150)
        self.table_widget.setColumnWidth(self.table_model.head["path"], 200)
        self.table_widget.setColumnWidth(self.table_model.head["in"], 200)
        self.table_widget.setColumnWidth(self.table_model.head["un"], 200)
        self.table_widget.doubleClicked.connect(self.changeValue)

        self.resize(870, 385)
        self.setWindowTitle("Edit Configure Option")

        self.addValue()

    def addValue(self):
        for key, install_v in Command.install.items():
            uninstall_v = Command.uninstall.get(key)
            path = Command.path.get(key)
            self.table_model.appendData(key, path, install_v, uninstall_v)

    def changeValue(self, index, isNew=False):
        # print "changeValue"
        row = index.row()
        column = self.table_model.columnCount()
        v = []
        for col in range(column):
            v.append(self.table_model.data(self.table_model.index(row, col)))

        cc_widget = ChangeConfiglDg(self, isNew, *v)
        while cc_widget.exec_():
            if not cc_widget.keyText:
                QtGui.QMessageBox.warning(cc_widget, "App Name is Empty!",
                                          "<b>App Name is Empty!</b><br>Reference instructions.")
                continue

            for col, value in zip(range(column), cc_widget.getValue):
                self.table_model.setData(
                    self.table_model.index(row, col), value
                )
            break

        else:
            if isNew:
                self.table_model.removeRow(self.table_model.rowCount() - 1)

    def newConfigHandle(self):
        super(JEditConfigWidget, self).newConfigHandle()
        index = self.table_model.indexFromItem(
            self.table_model.item(self.table_model.rowCount() - 1)
        )

        self.changeValue(index, True)

    def editConfigHandle(self):
        super(JEditConfigWidget, self).editConfigHandle()
        if self.selectItem:
            self.changeValue(self.selectItem)

    def backupConfigHandle(self):
        super(JEditConfigWidget, self).backupConfigHandle()
        Command.removeCommand()
        for key, value in self.getListValue().items():
            Command.setCommand(key, *value)

        now = datetime.datetime.now()
        time = now.strftime('%Y-%m-%d %H-%M-%S')

        path = QtGui.QFileDialog.getSaveFileName(
            self, "Backup Configure",
            "FFM RF Configure Backup",
            "Configure file (*.ini)"
        )[0]

        if not path:
            return

        n = os.path.splitext(path)
        name = n[0] + " " + time + n[1]

        try:
            handle.copyFile(FILE.CONFIG, name)
        except Exception as e:
            util.JLOG.error(e)

    def getListValue(self):
        # print "getListValue"
        res = dict()
        for row in range(self.table_model.rowCount()):
            if not self.table_model.item(row):
                continue

            path_text = ""
            if self.table_model.item(row, self.table_model.head["path"]):
                path_text = self.table_model.item(
                    row, self.table_model.head["path"]).text()

            in_text = ""
            if self.table_model.item(row, self.table_model.head["in"]):
                in_text = self.table_model.item(
                    row, self.table_model.head["in"]).text()

            un_text = ""
            if self.table_model.item(row, self.table_model.head["un"]):
                un_text = self.table_model.item(
                    row, self.table_model.head["un"]).text()

            res[self.table_model.item(row).text()] = \
                [path_text, in_text, un_text]

        return res


# class JEditPathWidget(JEditBase):
#     def __init__(self, parent=None):
#         super(JEditPathWidget, self).__init__(parent)
#
#         self.table_model = PathModel()
#         self.table_widget.setModel(self.table_model)
#         self.table_widget.setColumnWidth(self.table_model.head["key"], 200)
#         self.table_widget.setColumnWidth(self.table_model.head["path"], 400)
#
#         self.resize(720, 385)
#         self.setWindowTitle("Edit App Check Path")
#
#         self.addValue()
#
#     def addValue(self):
#         for key, path in Command.path.items():
#             self.table_model.appendData(key, path)
#
#     def getListValue(self):
#         print "getListValue"
#         res = dict()
#         for row in range(self.table_model.rowCount()):
#             if not self.table_model.item(row):
#                 continue
#
#             path_text = ""
#             if self.table_model.item(row, self.table_model.head["path"]):
#                 path_text = self.table_model.item(
#                     row, self.table_model.head["path"]).text()
#
#             res[self.table_model.item(row).text()] = path_text
#
#         return res
