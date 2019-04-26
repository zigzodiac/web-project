# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/9 18:16"
__all__ = ["__version__", ]
__version__ = "1.0.0"

import os, sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from config import FILE
from widget.ui_load import UILoader
from model.config_command import Command
from model.select_install_model import SelectInstallModel



class SelectInstallDg(QtGui.QDialog):
    def __init__(self, parent=None):
        super(SelectInstallDg, self).__init__(parent)
        self.initUI()

    def initUI(self):
        win = UILoader(os.path.join(os.path.dirname(__file__), os.pardir, FILE.UI_SELECT_INSTALL_DG),
                       os.path.join(os.path.dirname(__file__), os.pardir, FILE.CSS_MAIN))

        self.list_view = win.findChild(QtGui.QListView, "listView")
        self.list_model = SelectInstallModel(self)
        self.list_view.setModel(self.list_model)

        self.select_box = win.findChild(QtGui.QCheckBox, "checkBox")
        self.select_box.clicked.connect(self.selectBoxStateChangeHandle)

        btn_box = win.findChild(QtGui.QDialogButtonBox, "buttonBox")
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

        l = win.findChild(QtGui.QLayout, "gridLayout")
        self.setLayout(l)

        self.resize(win.width(), win.height())
        self.setWindowTitle(win.windowTitle())

        self.addValue()

    def addValue(self):
        Command.updateCommand()
        for key in Command.install.keys():
            self.list_model.appendData(key)

    def selectBoxStateChangeHandle(self):
        state = QtCore.Qt.Checked if self.select_box.checkState() else QtCore.Qt.Unchecked

        for item in self.list_model.getAllItems:
            item.setCheckState(state)

    @property
    def selectValue(self):
        l = []
        for i in range(self.list_model.rowCount()):
            item = self.list_model.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                l.append(item.text())
        return l