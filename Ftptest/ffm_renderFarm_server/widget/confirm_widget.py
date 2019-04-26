# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/14 17:44"
__all__ = ["__version__", "ConfirmDg"]
__version__ = "1.0.0"

import os, sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from widget.ui_load import UILoader
from config import FILE


class ConfirmDg(QtGui.QDialog):
    def __init__(self, command, data, parent=None):
        super(ConfirmDg, self).__init__(parent)
        self.data = data

        win = UILoader(os.path.join(os.path.dirname(__file__), os.pardir, FILE.UI_CONFIRM),
                       os.path.join(os.path.dirname(__file__), os.pardir, FILE.CSS_MAIN))

        self.list_widget = win.findChild(QtGui.QListWidget, "listWidget")

        btn_box = win.findChild(QtGui.QDialogButtonBox, "buttonBox")
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

        l = win.findChild(QtGui.QLayout, "gridLayout")
        self.setLayout(l)

        self.resize(win.width(), win.height())
        self.setWindowTitle(command)

        self.addData()

    def addData(self):
        for d in self.data:
            self.list_widget.addItem("%s: %s" % (d[0], ", ".join(d[1])))




