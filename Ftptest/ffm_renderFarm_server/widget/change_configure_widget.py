# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/10 16:32"
__all__ = ["__version__", ]
__version__ = "1.0.0"

import os, sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from config import FILE
from widget.ui_load import UILoader



class ChangeConfiglDg(QtGui.QDialog):
    def __init__(self, parent, isNew, key, path, install_text, uninstall_text):
        super(ChangeConfiglDg, self).__init__(parent)

        win = UILoader(os.path.join(os.path.dirname(__file__), os.pardir, FILE.UI_CHANGE_CONFIG),
                       os.path.join(os.path.dirname(__file__), os.pardir, FILE.CSS_MAIN))

        self.key_line = win.findChild(QtGui.QLineEdit, "keyLine")
        self.key_line.setText(key)
        self.path_line = win.findChild(QtGui.QLineEdit, "pathLine")
        self.path_line.setText(path)
        self.install_line = win.findChild(QtGui.QLineEdit, "installLine")
        self.install_line.setText(install_text)
        self.uninstall_line = win.findChild(QtGui.QLineEdit, "uninstallLine")
        self.uninstall_line.setText(uninstall_text)

        change_btn = win.findChild(QtGui.QPushButton, "changeBtn")
        change_btn.clicked.connect(self.keyLinePolicy)

        if isNew:
            change_btn.hide()
            self.key_line.setFocus()
            self.key_line.setReadOnly(False)

        btn_box = win.findChild(QtGui.QDialogButtonBox, "buttonBox")
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

        l = win.findChild(QtGui.QLayout, "gridLayout")
        self.setLayout(l)

        self.resize(win.width(), win.height())
        self.setWindowTitle(win.windowTitle() + " [%s]" % key)

    def keyLinePolicy(self):
        self.key_line.setReadOnly(False)
        self.setFocusProxy(self.key_line)

    @property
    def keyText(self):
        return self.key_line.text()

    @property
    def pathText(self):
        return self.path_line.text()

    @property
    def installText(self):
        return self.install_line.text()

    @property
    def uninstallText(self):
        return self.uninstall_line.text()

    @property
    def getValue(self):
        l = [self.keyText, self.pathText, self.installText, self.uninstallText]
        return l