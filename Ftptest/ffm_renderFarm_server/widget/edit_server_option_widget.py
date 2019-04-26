# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/15 14:08"
__all__ = ["__version__", ]
__version__ = "1.0.0"

import os, sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from widget.ui_load import UILoader
from config import FILE
from util.jlog import LOG_LEVEL_KEY
import util


class JEditServerOptionDg(QtGui.QDialog):
    def __init__(self, ip, port, level, path, parent=None):
        super(JEditServerOptionDg, self).__init__(parent)
        self.__combo_text = ""

        win = UILoader(os.path.join(os.path.dirname(__file__), os.pardir, FILE.UI_EDIT_SERVER),
                       os.path.join(os.path.dirname(__file__), os.pardir, FILE.CSS_MAIN))

        self.setWindowTitle(win.windowTitle())
        l = win.findChild(QtGui.QLayout, "gridLayout")
        self.setLayout(l)
        self.setFixedSize(win.width(), win.height())

        self.ip_line = self.findChild(QtGui.QLineEdit, "IPLine")
        self.ip_line.setText(str(ip))
        self.port_line = self.findChild(QtGui.QLineEdit, "portLine")
        self.port_line.setText(str(port))

        self.log_line = self.findChild(QtGui.QLineEdit, "logFileLine")
        self.log_line.setText(str(path))

        choose_log_btn = self.findChild(QtGui.QPushButton, "chooseLogBtn")
        choose_log_btn.clicked.connect(self.chooseLogHandle)

        self.combo_box = self.findChild(QtGui.QComboBox, "comboBox")
        self.combo_box.activated.connect(self.comboBoxSelectItemHandle)
        self.combo_box.addItems(LOG_LEVEL_KEY)

        i = 0
        if level in LOG_LEVEL_KEY:
            self.__combo_text = level
            i = self.combo_box.findText(level)
        self.combo_box.setCurrentIndex(i)

        btn_box = self.findChild(QtGui.QDialogButtonBox, "buttonBox")
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

    def comboBoxSelectItemHandle(self, index):
        self.__combo_text = self.combo_box.itemText(index)

    def chooseLogHandle(self):
        # print "chooseLogHandle"
        file = QtGui.QFileDialog.getSaveFileName(self, "Choose Log File", self.logText)[0]
        if file:
            self.log_line.setText(file)

    @property
    def comboText(self):
        return self.__combo_text

    @property
    def IPText(self):
        return self.ip_line.text()

    @property
    def portText(self):
        return self.port_line.text()

    @property
    def logText(self):
        return self.log_line.text()

