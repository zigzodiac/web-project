# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/25 11:10"
__all__ = ["__version__", "ManageConfigDg"]
__version__ = "1.0.0"

import os, sys
from collections import OrderedDict
import PySide.QtGui as QtGui

from config import FILE
from widget.add_soft_dialog import AddSoftDg
import widget
import model



class ManageConfigDg(QtGui.QDialog):
    HEAD = OrderedDict([
        ("Name", 0),
        ("Versions", 1),
    ])

    def __init__(self, parent=None):
        super(ManageConfigDg, self).__init__(parent)
        self.initUI()
        self.loadData()

    def initUI(self):
        ui_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.UI_MANAGE_CONFIG)
        css_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.CSS_MAIN)
        win = widget.UILoader(ui_file, css_file)

        self.resize(win.width(), win.height())
        self.setStyleSheet(win.styleSheet())
        main_icon = os.path.join(os.path.dirname((__file__)), os.pardir, FILE.ICON_MAIN)
        self.setWindowIcon(QtGui.QIcon(main_icon))
        self.setWindowTitle("Manage Configure Dialog")
        l = win.findChild(QtGui.QLayout, "gridLayout")
        self.setLayout(l)

        self.path_line = self.findChild(QtGui.QLineEdit, "ftpPathLine")
        self.id_line = self.findChild(QtGui.QLineEdit, "ftpIDLine")
        self.pwd_line = self.findChild(QtGui.QLineEdit, "ftpPwdLine")

        addBtn = self.findChild(QtGui.QPushButton, "softAddBtn")
        addBtn.clicked.connect(self.addSoftHandle)
        delBtn = self.findChild(QtGui.QPushButton, "softDelBtn")
        delBtn.clicked.connect(self.delSoftHandle)

        self.soft_table = self.findChild(QtGui.QTableWidget, "softTable")
        self.soft_table.setHorizontalHeaderLabels(self.HEAD.keys())

        btn_box = self.findChild(QtGui.QDialogButtonBox, "buttonBox")
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

    def loadData(self):
        self.path_line.setText(model.DB_CONFIGURE.ftpPath)
        self.id_line.setText(model.DB_CONFIGURE.ftpID)
        self.pwd_line.setText(model.DB_CONFIGURE.ftpPassword)

        self.addTableItem(model.DB_CONFIGURE.software)

    def addTableItem(self, data):
        for soft_name in data:
            if not isinstance(data[soft_name], dict):
                continue

            if not data[soft_name].get("Versions"):
                continue

            row = self.soft_table.rowCount()
            self.soft_table.insertRow(row)
            name_item = QtGui.QTableWidgetItem(soft_name)
            ver_item = QtGui.QTableWidgetItem(", ".join(data[soft_name]["Versions"]))

            self.soft_table.setItem(row, self.HEAD["Name"], name_item)
            self.soft_table.setItem(row, self.HEAD["Versions"], ver_item)

    @property
    def selectTableItem(self):
        items = self.soft_table.selectedItems()
        if items:
            return items[0]

    def addSoftHandle(self):
        # print "addSoftHandle"
        asdg = AddSoftDg(self)
        if asdg.exec_():
            if not asdg.nameText or not asdg.versionList:
                return
            info = {asdg.nameText: {"Name": asdg.nameText, "Versions": asdg.versionList}}
            self.addTableItem(info)

    def delSoftHandle(self):
        # print "delSoftHandle"
        if not self.selectTableItem:
            return
        soft_name = self.selectTableItem.text()
        warning_notice = "Are you sure want to delete soft <b>%s</b>? " \
                         "<br>Notice: It cannot be restored after " \
                         "deletion." % soft_name
        reply = QtGui.QMessageBox.question(self, "Delete Warning",
                                           warning_notice,
                                           QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No
                                           )

        if reply == QtGui.QMessageBox.Yes:
            self.soft_table.removeRow(self.selectTableItem.row())

    @property
    def FTPPath(self):
        return self.path_line.text()

    @property
    def FTPID(self):
        return self.id_line.text()

    @property
    def FTPPassword(self):
        return self.pwd_line.text()

    @property
    def SoftwareInfo(self):
        res = {}
        for i in range(self.soft_table.rowCount()):
            name = self.soft_table.item(i, self.HEAD["Name"]).text().upper()
            version = (self.soft_table.item(i, self.HEAD["Versions"]).text()).split(", ")
            res.update({name: {"Name": name, "Versions": version}})
        return res