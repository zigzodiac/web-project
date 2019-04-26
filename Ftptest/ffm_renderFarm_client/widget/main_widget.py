# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/3 10:30"
__all__ = ["__version__", ]
__version__ = "1.0.0"

import os, sys
import time
import connect
from connect.run_client import ConnectThread
from connect import protocol
import widget
import config
from config.logger import Logger
from path.versions import Viersions
from ffm.config.jconfig import JConfig

import subprocess
import PySide.QtUiTools as QtUiTools
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui


def UILoader(UI_File, css_name=None):
    '''Load UI file'''
    loader = QtUiTools.QUiLoader()   # 创建一个UILoader
    ui_file = QtCore.QFile(UI_File)  # 加载UI文件路径
    ui_file.open(QtCore.QFile.ReadOnly)   # 设置只读模式打开文件
    window = loader.load(ui_file)   # 将读取出的框架绑定到py变量
    ui_file.close()   # 关闭文件，加载成功
    if css_name:
        with open(css_name, 'r') as css_file:
            style_sheet = css_file.read()
        window.setStyleSheet(style_sheet)
    return window


class JMainWindow(QtCore.QObject):
    def __init__(self, address):
        super(JMainWindow, self).__init__()
        ui_file = os.path.join(config.MAIN_PATH, 'resource/ui/mainWindow.ui')
        css_file = os.path.join(config.MAIN_PATH, 'resource/css/main.css')

        self.main_ui = UILoader(ui_file, css_file)
        self.main_ui. setWindowTitle("FFM_RenderFarm_Client")
        self.main_ui.setWindowIcon(QtGui.QIcon("resource/images/ffm_main.png"))

        self.ip_edit = self.main_ui.findChild(QtGui.QLineEdit, 'ip_edit')
        self.port_edit = self.main_ui.findChild(QtGui.QLineEdit, 'port_edit')
        self.status_label = self.main_ui.findChild(QtGui.QLabel, 'status_label')
        self.apps_label = self.main_ui.findChild(QtGui.QLabel, 'apps_label')
        self.reconnect_button = self.main_ui.findChild(QtGui.QPushButton, 'reconnect_button')
        self.disconnect_button = self.main_ui.findChild(QtGui.QPushButton, 'disconnect_button')
        self.manual_button = self.main_ui.findChild(QtGui.QPushButton, 'manual_button')

        self.manual_button.clicked.connect(self.__mconnectEvent)
        self.disconnect_button.clicked.connect(self.__disconnectEvent)
        self.reconnect_button.clicked.connect(self.__reconnectEvent)

        self.__setUI()
        self.setStatus("Disconnect")

        self.address = address
        self.thread = connect_server(self.address)

    def __setIp(self):
        self.ip_edit.setText(config.SERVER_IP)
        ip_rx = QtCore.QRegExp("^((2[0-4]\\d|25[0-5]|[01]?\\d\\d?)\\.){3}(2[0-4]\\d|25[0-5]|[01]?\\d\\d?)$")
        pValidator = QtGui.QRegExpValidator(ip_rx)
        self.ip_edit.setValidator(pValidator)

    def __setPort(self):
        self.port_edit.setText(str(config.SERVER_PORT))
        port_rx = QtCore.QRegExp("[0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{4}|65[0-4]\d{2}|655[0-2]\d|6553[0-5]")
        pValidator = QtGui.QRegExpValidator(port_rx)
        self.port_edit.setValidator(pValidator)

    def setApps(self):
        app_str = ''

        apps = Viersions().getVersions()
        for app in apps:
            app_str += app + ' \n'
        self.apps_label.setText(app_str)

        if connect.Client != None:
            connect.Client.send_message(
                connect.packMessage(
                    protocol.MessageType.update_app.value,
                    apps.keys()
                )
            )

    def __setUI(self):
        self.__setIp()
        self.__setPort()
        self.setApps()

    def setStatus(self, status):
        self.status_label.setText(status)

    def getIp(self):
        return str(self.ip_edit.text())

    def getPort(self):
        return int(self.port_edit.text())

    def show(self):
        self.main_ui.show()

    def __mconnectEvent(self):
        self.__disconnectEvent()

        if not self.thread:
            self.thread = connect_server((self.getIp(), self.getPort()))

    def __disconnectEvent(self):
        print "DISCONN", self.thread
        if self.thread:
            self.thread.stop()
            self.thread.join()
            self.thread = None
            connect.Client = None
            self.setStatus('Disconnect')

    def __reconnectEvent(self):
        self.__disconnectEvent()

        con = JConfig(config.CONFIG_FILE)
        config.SERVER_IP = con.getConfig('Server', 'IP')
        config.SERVER_PORT = int(con.getConfig('Server', 'PORT'))

        if not self.thread:
            self.thread = connect_server((config.SERVER_IP, config.SERVER_PORT))

        self.ip_edit.setText(config.SERVER_IP)
        self.port_edit.setText(str(config.SERVER_PORT))

        self.setApps()


def connect_server(address):
    t1 = ConnectThread(address)
    t1.setDaemon(True)
    t1.start()
    return t1


class ClientReceive(QtCore.QObject):
    WELCOME_SIGNAL = QtCore.Signal(str)
    UNINSTALL_SIGNAL = QtCore.Signal(list)
    INSTALL_SIGNAL = QtCore.Signal(list)
    RESTART_SIGNAL = QtCore.Signal(str)
    RESEND_SIGNAL = QtCore.Signal()

    def __init__(self):
        super(ClientReceive, self).__init__()
        self.WELCOME_SIGNAL.connect(self.__welcomeEvent)
        self.UNINSTALL_SIGNAL.connect(self.__uninstallEvent)
        self.INSTALL_SIGNAL.connect(self.__installEvent)
        self.RESTART_SIGNAL.connect(self.__restartEvent)
        self.RESEND_SIGNAL.connect(self.__resendEvent)

        self.commands = set()
        self.popen = None

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.__timerEvent)

        self.update_timer = QtCore.QTimer(self)
        self.update_timer.timeout.connect(self.updateAppEvent)

    def __welcomeEvent(self, _str):
        config.CONFIG_FILE = _str

    def __uninstallEvent(self, lst):
        for app_name in lst:
            try:
                command = JConfig(config.CONFIG_FILE).getConfig(config.UNINSTALL, app_name)
                self.commands.add(command)
            except Exception as e:
               Logger.error(e)

        self.timer.start(3000)

    def __installEvent(self, lst):
        for app_name in lst:
            try:
                command = JConfig(config.CONFIG_FILE).getConfig(config.INSTALL, app_name)
                self.commands.add(command)
            except Exception as e:
                Logger.error(e)

        self.timer.start(3000)

    def __restartEvent(self, _str):
        os.system(_str)

    def __resendEvent(self):
        widget.JWindow.setApps()

    def __timerEvent(self):
        if not self.popen:
            try:
                if len(self.commands):
                    command = self.commands.pop()
                    Logger.info(command)
                    self.popen = subprocess.Popen(command)
            except Exception as e:
                self.popen = None
                Logger.error(e)
        else:
            if self.popen.poll() != None:
                Logger.info(self.popen.poll())
                Logger.info('one is ok')
                self.popen = None
                self.update_timer.start(10000)

        if len(self.commands) == 0 and self.popen == None:
            self.timer.stop()
            Logger.info('commands are ok')

    def updateAppEvent(self):
        widget.JWindow.setApps()
        self.update_timer.stop()


def run(address):

    app = QtGui.QApplication(sys.argv)
    win = JMainWindow(address)
    widget.JWindow = win
    widget.JClientReceive = ClientReceive()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    pass



