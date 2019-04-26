# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/2 16:09"
__all__ = ["__version__", "JMainWindow"]
__version__ = "1.0.0"

import os, sys
from collections import OrderedDict
import webbrowser
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
from ffm.config.jconfig import JConfig

from config import FILE, PARAM, CONFIG
from connect.run_server import ConnectThread
from connect import protocol
from widget.ui_load import UILoader
from widget.show_configure_widget import JEditConfigWidget
from widget.select_install_widget import SelectInstallDg
from widget.confirm_widget import ConfirmDg
from widget.edit_server_option_widget import JEditServerOptionDg
from model.select_item import JSelectItem
from model.config_command import Command
from util.jlog import JLog
import util
import widget
import connect



class JMainWindow(QtGui.QMainWindow):
    CONNECT_SIGNAL = QtCore.Signal(dict)
    DISCONNECT_SIGNAL = QtCore.Signal(dict)
    UPDATE_APP_SIGNAL = QtCore.Signal(dict)

    HEAD = {
        "name": 0,
        "ip": 1,
        "app": 2,
    }

    COMBO_TEXT = OrderedDict([
        ("none", ""),
        ("update", "Update Client"),
        ("sep", "-" * 15),
        ("restart", "Restart Client"),
    ])

    def __init__(self, connectThreadFunc, ip, port, parent=None):
        super(JMainWindow, self).__init__(parent)
        self.select_parent_item = set()
        self.select_child_item = JSelectItem()
        self.__send_command_to_client = ""
        self.comboText = ["none", "update", "sep", "restart"]
        self.connectThreadFunc = connectThreadFunc
        self.initUI()
        self.resize(800, 600)
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), os.pardir, FILE.ICON_MAIN)))
        self.CONNECT_SIGNAL.connect(self.clientConnectHandle)
        self.DISCONNECT_SIGNAL.connect(self.clientDisconnectHandle)
        self.UPDATE_APP_SIGNAL.connect(self.updateAppHandle)

        self.connect_thread = connectThreadFunc(ip, port)

    def initUI(self):
        window = UILoader(os.path.join(os.path.dirname(__file__), os.pardir, FILE.UI_MAIN_WINDOW),
                          os.path.join(os.path.dirname(__file__), os.pardir, FILE.CSS_MAIN))

        self.path_line = window.findChild(QtGui.QLineEdit, "pathLine")
        open_btn = window.findChild(QtGui.QPushButton, "openBtn")
        open_btn.clicked.connect(self.openBtnHandle)

        install_btn = window.findChild(QtGui.QPushButton, "installBtn")
        install_btn.clicked.connect(self.installHandle)

        uninstall_btn = window.findChild(QtGui.QPushButton, "unInstallBtn")
        uninstall_btn.clicked.connect(self.uninstallHandle)

        do_btn = window.findChild(QtGui.QPushButton, "doBtn")
        do_btn.clicked.connect(self.sendCommand2ClientHandle)

        self.combo_box = window.findChild(QtGui.QComboBox, "comboBox")
        self.combo_box.activated.connect(self.comboBoxSelectItemHandle)
        self.combo_box.addItems(self.COMBO_TEXT.values())

        self.tree_widget = window.findChild(QtGui.QTreeWidget, "treeWidget")
        self.tree_widget.itemChanged.connect(self.onCheckStateChangeItem)
        self.tree_widget.setColumnWidth(self.HEAD["name"], 200)

        self.select_box = window.findChild(QtGui.QCheckBox, "checkBox")
        self.select_box.clicked.connect(self.selectBoxStateChangeHandle)

        self.selected_label = window.findChild(QtGui.QLabel, "selectedLabel")
        self.total_label = window.findChild(QtGui.QLabel, "totalLabel")

        edit_configure_option = window.findChild(QtGui.QAction, "actionEdit_Configure_Option")
        edit_configure_option.activated.connect(self.editConfigureOptionHandle)

        edit_server_option = window.findChild(QtGui.QAction, "actionEdit_Server_Option")
        edit_server_option.activated.connect(self.editServerOptionHandle)

        instructions = window.findChild(QtGui.QAction, "actionInstall_package")
        instructions.setIcon(QtGui.QIcon(
            os.path.join(os.path.dirname(__file__), os.pardir, FILE.ICON_HELP))
        )
        instructions.triggered.connect(self.packageInstructions)

        readme = window.findChild(QtGui.QAction, "actionFFM_RFM")
        readme.setIcon(QtGui.QIcon(
            os.path.join(os.path.dirname(__file__), os.pardir, FILE.ICON_HELP))
        )
        readme.triggered.connect(self.readme)

        about = window.findChild(QtGui.QAction, "actionAbout")
        about.setIcon(QtGui.QIcon(
            os.path.join(os.path.dirname(__file__), os.pardir, FILE.ICON_INFO))
        )
        about.triggered.connect(self.about)

        self.setCentralWidget(window)
        self.setWindowTitle(window.windowTitle())

    def clientDisconnectHandle(self, data):
        # print "disconnect", data
        l = []
        for i in range(self.tree_widget.topLevelItemCount()):
            if data[PARAM.NAME] == self.tree_widget.\
                    topLevelItem(i).text(self.HEAD["name"])\
                    and data[PARAM.IP] == self.tree_widget.\
                    topLevelItem(i).text(self.HEAD["ip"]):
                l.insert(0, i)

        for i in l:
            self.tree_widget.takeTopLevelItem(i)

        try:
            self.select_parent_item.remove(data[PARAM.NAME])
        except:
            pass

        del self.select_child_item[data[PARAM.NAME]]
        self.updateCheckBox()

    def clientConnectHandle(self, data):
        client = connect.clients.get_s(data[PARAM.NAME])
        client.send_message(
            connect.packMessage(
                protocol.MessageType.welcome.value,
                Command.configFile
            )
        )

        pc_item = self.createTreeItem(data)
        self.tree_widget.addTopLevelItem(pc_item)
        self.tree_widget.sortItems(self.HEAD["name"], QtCore.Qt.AscendingOrder)
        self.total_label.setText(str(self.tree_widget.topLevelItemCount()))
        self.updateCheckBox()

    def updateAppHandle(self, data):
        # print data
        item = self.tree_widget.findItems(data[PARAM.NAME], QtCore.Qt.MatchFixedString)
        if item:
            if len(item) > 1:
                for i in range(len(item), 1, -1):
                    self.tree_widget.takeTopLevelItem(i)

            item = item[0]
            item.takeChildren()

            item.setData(self.HEAD["app"], QtCore.Qt.EditRole, ", ".join(data[PARAM.APPS]))
            self.createChildItem(item, data[PARAM.APPS], item.checkState(self.HEAD["name"]))

    def createTreeItem(self, data):
        item = QtGui.QTreeWidgetItem()
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)

        item.setCheckState(self.HEAD["name"], QtCore.Qt.Unchecked)

        item.setData(self.HEAD["name"], QtCore.Qt.EditRole, data[PARAM.NAME])
        item.setData(self.HEAD["ip"], QtCore.Qt.EditRole, data[PARAM.IP])
        item.setData(self.HEAD["app"], QtCore.Qt.EditRole, ", ".join(data[PARAM.APPS]))

        self.createChildItem(item, data[PARAM.APPS])

        return item

    def createChildItem(self, parentItem, data, state=QtCore.Qt.Unchecked):
        del self.select_child_item[parentItem.text(self.HEAD["name"])]

        for app in data:
            app_item = QtGui.QTreeWidgetItem()
            app_item.setFlags(app_item.flags() | QtCore.Qt.ItemIsUserCheckable)
            app_item.setCheckState(self.HEAD["app"], state)
            app_item.setData(self.HEAD["app"], QtCore.Qt.EditRole, app)
            parentItem.addChild(app_item)

            if state == QtCore.Qt.Checked:
                self.select_child_item.update(
                    parentItem.text(self.HEAD["name"]),
                    app_item.text(self.HEAD["app"])
                )

    # def getSubtreeItems(self, treeItem):
    #     items = []
    #     items.append(treeItem)
    #     for i in range(treeItem.childCount()):
    #         items.extend(self.getSubtreeItems(treeItem.child(i)))
    #     return items

    def getAllTreeItems(self):
        all_items = []
        for i in range(self.tree_widget.topLevelItemCount()):
            all_items.append(self.tree_widget.topLevelItem(i))
            # all_items.extend(self.getSubtreeItems(top_item))
        return all_items

    def setTreeItemsCheckState(self, name, state):
        item = self.tree_widget.findItems(name, QtCore.Qt.MatchFixedString)
        if item:
            item = item[0]
            item.setCheckState(self.HEAD["name"], state)

    def setChildItemCheckState(self, item, state):
        for i in range(item.childCount()):
            childItem = item.child(i)
            childItem.setCheckState(self.HEAD["app"], state)

            # if state == QtCore.Qt.Checked:
            #     self.select_child_item.update(
            #         item.text(self.HEAD["name"]),
            #         childItem.text(self.HEAD["app"])
            #     )
            # else:
            #     self.select_child_item.delete(
            #         item.text(self.HEAD["name"]),
            #         childItem.text(self.HEAD["app"])
            #     )

    def onCheckStateChangeItem(self, item, column):
        state = item.checkState(column)

        if item.parent():
            if item.checkState(self.HEAD["app"]) == QtCore.Qt.Checked:
                self.select_child_item.update(
                    item.parent().text(self.HEAD["name"]),
                    item.text(self.HEAD["app"])
                )
                item.parent().setCheckState(self.HEAD["name"], QtCore.Qt.Checked)
            else:
                self.select_child_item.delete(
                    item.parent().text(self.HEAD["name"]),
                    item.text(self.HEAD["app"])
                )

                _f = False
                for i in range(item.parent().childCount()):
                    childItem = item.parent().child(i)
                    if childItem.checkState(self.HEAD["app"]) == QtCore.Qt.Checked:
                        _f = True
                        break

                if not _f:
                    item.parent().setCheckState(self.HEAD["name"], QtCore.Qt.Unchecked)
        else:
            self.setChildItemCheckState(item, state)
            if item.checkState(self.HEAD["name"]) == QtCore.Qt.Checked:
                self.select_parent_item.add(item.text(self.HEAD["name"]))
            else:
                try:
                    self.select_parent_item.remove(item.text(self.HEAD["name"]))
                except:
                    pass

        self.updateCheckBox()

    def updateCheckBox(self):
        self.total_label.setText(str(self.tree_widget.topLevelItemCount()))
        self.selected_label.setText(str(len(self.select_parent_item)))

        if self.selected_label.text() == self.total_label.text() != '0':
            self.select_box.setCheckState(QtCore.Qt.Checked)
        else:
            self.select_box.setCheckState(QtCore.Qt.Unchecked)

    def selectBoxStateChangeHandle(self):
        state = QtCore.Qt.Checked if self.select_box.checkState() else QtCore.Qt.Unchecked

        for item in self.getAllTreeItems():
            item.setCheckState(self.HEAD["name"], state)
            self.setChildItemCheckState(item, state)

    def openBtnHandle(self):
        si_dg = SelectInstallDg(self)
        if si_dg.exec_():
            if si_dg.selectValue:
                self.path_line.setText("; ".join(si_dg.selectValue))
                return
        self.path_line.setText("")

    def editServerOptionHandle(self):
        # print "editServerOptionHandle"
        Command.updateCommand()
        ip, port = Command.IP, Command.port
        con_base = JConfig(FILE.CONFIG)
        level = con_base.getConfig("Log", "level")
        path = con_base.getConfig("Log", "file")

        es_dg = JEditServerOptionDg(ip, port, level, path, self)
        if es_dg.exec_():
            if es_dg.comboText:
                log_level = es_dg.comboText
            else:
                log_level = "DEBUG"

            if es_dg.logText == path:
                log_path = path
            else:
                log_path = es_dg.logText
                con_base.setConfig("Log", "file", log_path)
            log_name = con_base.getConfig("Log", "name")
            con_base.setConfig("Log", "level", log_level)
            FILE.FILE_LOG = log_path
            util.JLOG = JLog(log_path, log_level, log_name)

            IP = es_dg.IPText
            port = es_dg.portText

            Command.IP, Command.port = IP, port
            Command.config.setConfig(CONFIG.SEC_SERVER, CONFIG.KEY_IP, IP)
            Command.config.setConfig(CONFIG.SEC_SERVER, CONFIG.KEY_PORT, str(port))

            # print self.connect_thread
            # self.connect_thread.stop()

            # self.connect_thread = self.connectThreadFunc(IP, int(port))

            # print self.connect_thread

    def editConfigureOptionHandle(self):
        # print "editConfigureOptionHandle"
        Command.updateCommand()
        ec_widget = JEditConfigWidget(self)
        if ec_widget.exec_():
            Command.removeCommand()
            for key, value in ec_widget.getListValue().items():
                Command.setCommand(key, *value)

    def sendCommand2ClientHandle(self):
        # print "sendCommand2ClientHandle"
        # print self.command2Client
        if self.command2Client == self.COMBO_TEXT["restart"]:
            self.restartClientHandle()
        elif self.command2Client == self.COMBO_TEXT["update"]:
            self.updateClientHandle()

        self.combo_box.setCurrentIndex(0)

    def comboBoxSelectItemHandle(self, index):
        # print "comboBoxSelectItemHandle"
        self.command2Client = self.combo_box.itemText(index)
        l = self.COMBO_TEXT.values()
        l.remove(self.COMBO_TEXT["none"])
        l.remove(self.COMBO_TEXT["sep"])
        if self.command2Client not in l:
            self.combo_box.setCurrentIndex(0)

    def installHandle(self):
        # print "installHandle"
        if not self.path_line.text():
            return

        if not self.select_parent_item:
            return

        install_list = self.path_line.text().split("; ")

        n = []
        for name in self.select_parent_item:
            client = connect.clients.get_s(name)
            util.JLOG.printInfo("install command: client name '" + name + "'", install_list)
            client.send_message(
                connect.packMessage(
                    protocol.MessageType.install.value,
                    install_list
                )
            )
            n.append(name)

        for name in n:
            self.setTreeItemsCheckState(name, QtCore.Qt.Unchecked)

    def uninstallHandle(self):
        # print "uninstallHandle"
        cf_dg = ConfirmDg("UnInstall List", self.select_child_item, self)
        if cf_dg.exec_():
            n = []
            for name in self.select_child_item.keys():
                client = connect.clients.get_s(name)
                util.JLOG.printInfo("uninstall command: client name '" + name + "'", list(self.select_child_item[name]))
                client.send_message(
                    connect.packMessage(
                        protocol.MessageType.uninstall.value,
                        list(self.select_child_item[name])
                    )
                )
                n.append(name)

            for name in n:
                self.setTreeItemsCheckState(name, QtCore.Qt.Unchecked)

    def restartClientHandle(self):
        # print "restartClientHandle"
        if not self.select_parent_item:
            return

        n = []
        for name in self.select_parent_item:
            client = connect.clients.get_s(name)
            client.send_message(
                connect.packMessage(
                    protocol.MessageType.restart.value,
                    Command.restartCommand
                )
            )
            n.append(name)

        for name in n:
            self.setTreeItemsCheckState(name, QtCore.Qt.Unchecked)

    def updateClientHandle(self):
        # print "updateClientHandle"
        if not self.select_parent_item:
            return

        n = []
        for name in self.select_parent_item:
            client = connect.clients.get_s(name)
            client.send_message(
                connect.packMessage(
                    protocol.MessageType.update2client.value,
                    "update apps"
                )
            )
            n.append(name)

        for name in n:
            self.setTreeItemsCheckState(name, QtCore.Qt.Unchecked)

    @property
    def command2Client(self):
        return self.__send_command_to_client

    @command2Client.setter
    def command2Client(self, text):
        self.__send_command_to_client = text

    @staticmethod
    def readme():
        webbrowser.open(os.path.join(os.path.dirname(__file__), os.pardir,
                                     FILE.README))

    @staticmethod
    def packageInstructions():
        webbrowser.open(os.path.join(os.path.dirname(__file__), os.pardir,
                                     FILE.INSTALL_PACKAGE_INSTRUCTION))

    def about(self):
        with open(os.path.join(
                os.path.dirname(__file__), os.pardir, FILE.ABOUT), "rU") as f:
            contents = f.read()

        msg_box = QtGui.QMessageBox()
        msg_box.setIconPixmap(QtGui.QPixmap(FILE.ICON_MAIN))
        msg_box.about(self, "About FFM Render Farm Monitor",
                      u"%s" % contents.decode("utf8").replace("\n", "<br>"))





def connect_server(ip, port):
    t1 = ConnectThread(ip, port)
    t1.setDaemon(True)
    t1.start()
    return t1


def run(app, ip, port):
    win = JMainWindow(connect_server, ip, port)
    widget.JWindow = win
    # t = connect_server(ip, port)

    win.show()
    sys.exit(app.exec_())


