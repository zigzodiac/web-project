# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/25 13:51"
__all__ = ["__version__", "AddSoftDg"]
__version__ = "1.0.0"

import os, sys
import PySide.QtGui as QtGui

from config import FILE
import widget


class AddSoftDg(QtGui.QDialog):
    def __init__(self, parent=None):
        super(AddSoftDg, self).__init__(parent)
        ui_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.UI_ADD_SOFT_DG)
        css_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.CSS_MAIN)
        win = widget.UILoader(ui_file, css_file)

        self.setWindowTitle("Add Software version information")
        l = win.findChild(QtGui.QLayout, "gridLayout")
        self.setLayout(l)
        self.setFixedSize(win.width(), win.height())

        self.name_line = self.findChild(QtGui.QLineEdit, "nameLine")
        self.version_line = self.findChild(QtGui.QLineEdit, "versionLine")

        btn_box = self.findChild(QtGui.QDialogButtonBox, "buttonBox")
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

    @property
    def nameText(self):
        return self.name_line.text().upper()

    @property
    def versionList(self):
        flag = False
        res = []
        ver = self.version_line.text()
        l = ver.split(",")
        for v in l:
            v = v.strip()
            if v:
                flag = True
            res.append(v)

        if flag:
            return res
        else:
            return None




