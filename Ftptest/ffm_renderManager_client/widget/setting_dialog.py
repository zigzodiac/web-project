# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import config
import widget
from ffm.config.jconfig import JConfig
import connect
from connect import protocol
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
import datetime
import pprint
from widget.ftp import FtpDialog
# from ffm.file.jfile import MD5File
import util


class SettingDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(SettingDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowMaximizeButtonHint)

        self.ui_file = os.path.join(config.MAIN_PATH, 'resource/ui/setting.ui')
        css_file = os.path.join(config.MAIN_PATH, 'resource/css/main.css')
        self.main_ui = widget.UILoader(self.ui_file, css_file)

        self.setWindowTitle("Setting")
        self.setWindowIcon(QtGui.QIcon("resource/images/ffm_main.png"))

        self.buttonBox = self.main_ui.findChild(QtGui.QDialogButtonBox, 'buttonBox')
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.ip1 = self.main_ui.findChild(QtGui.QLineEdit, 'ip1')
        self.ip2 = self.main_ui.findChild(QtGui.QLineEdit, 'ip2')
        self.ip3 = self.main_ui.findChild(QtGui.QLineEdit, 'ip3')
        self.ip4 = self.main_ui.findChild(QtGui.QLineEdit, 'ip4')
        self.port = self.main_ui.findChild(QtGui.QLineEdit, 'port')

        self.main_layout = self.main_ui.findChild(QtGui.QLayout, "verticalLayout")
        self.setLayout(self.main_layout)
        self.setStyleSheet(self.main_ui.styleSheet())

        #
        con = JConfig(os.path.join(config.MAIN_PATH, 'renderManagerConfig.ini'))
        remember = con.getConfig('Server', 'ip')
        port = con.getConfig('Server', 'port')

        ip_list = str(remember).split('.')

        while len(ip_list) < 4:
            ip_list.append("")

        self.ip1.setText(ip_list[0])
        self.ip2.setText(ip_list[1])
        self.ip3.setText(ip_list[2])
        self.ip4.setText(ip_list[3])
        self.port.setText(port)

        re_ip = QtCore.QRegExp("\d{3}")
        pvalidator = QtGui.QRegExpValidator(re_ip)
        for _line in [self.ip1, self.ip2, self.ip3, self.ip4]:
            _line.setValidator(pvalidator)

    def getIp(self):
        ip = self.ip1.text() + '.' + self.ip2.text() + '.' + self.ip3.text() + '.' + self.ip4.text()
        return ip

    def getPort(self):
        return self.port.text()