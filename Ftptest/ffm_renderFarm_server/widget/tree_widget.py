# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/2 16:20"
__all__ = ["__version__", ]
__version__ = "1.0.0"

import os, sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from model.client_model import JClientModel
from widget.ui_load import UILoader


class JTreeWindow(QtGui.QTreeWidget):
    def __init__(self, parent=None):
        super(JTreeWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        pass
        # self.model = JClientModel()
        # self.setModel(self.model)
        # self.setColumnWidth(self.model.head["name"], 120)
        # self.setColumnWidth(self.model.head["ip"], 120)
        # self.setEditTriggers(False)






if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    t = JTreeWindow()
    t.show()
    sys.exit(app.exec_())
