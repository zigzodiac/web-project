# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
main window module, show main window include user table.
run function, pass in various configuration parameters.
start connect server thread.
"""
__author__ = "jeremyjone"
__datetime__ = "2019/3/7 22:56"
__all__ = ["__version__", "JMainWindow", "run"]
__version__ = "1.0.0"
import os, sys
import webbrowser
from dateutil import parser
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
from ffm.config.jconfig import JConfig
import threading

from database.db_handle import MangoDBHandle
from config import FILE, DB, PARAM
from connect import protocol
from connect.run_server import ConnectThread
import connect
from util import handle
from util.file_copy_handle import CopyHandle
from util.check_thread import CheckFileMD5
import util
from model.config_model import ConfigModel
import model
from widget.main_user_table import UserTable
from widget.manage_config_dialog import ManageConfigDg
from widget.manage_user_dialog import ManageUserDg
from widget.edit_user_dialog import EditUserDg
import widget


class JMainWindow(QtGui.QMainWindow):
    CONNECT_SIGNAL = QtCore.Signal(dict)
    DISCONNECT_SIGNAL = QtCore.Signal(dict)
    GET_FTP_SIGNAL = QtCore.Signal(dict)
    JOB_UPDATE_SIGNAL = QtCore.Signal(dict)
    GET_SOFT_VERSION_SIGNAL = QtCore.Signal(dict)
    GET_ERROR_SIGNAL = QtCore.Signal(dict)
    GET_FILE_VALID_SIGNAL = QtCore.Signal(dict)
    PAY_R_SIGNAL = QtCore.Signal(dict)

    SUBMIT_SIGNAL = QtCore.Signal(dict)
    JOB_SUBMIT_SIGNAL = QtCore.Signal(object)
    UPDATE_SIGNAL = QtCore.Signal(object)
    CANCEL_SIGNAL = QtCore.Signal(object)
    FINISH_SIGNAL = QtCore.Signal(object)
    CS_UPDATE_SIGNAL = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super(JMainWindow, self).__init__(parent)

        ui_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.UI_MAIN_WINDOW)
        # css_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.CSS_MAIN)
        css_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.CSS_MAIN)
        window = widget.UILoader(ui_file, css_file)
        self.setCentralWidget(window)
        self.setWindowTitle(window.windowTitle())
        self.resize(window.width(), window.height())
        self.setWindowIcon(QtGui.QIcon(FILE.ICON_MAIN))

        self.initUI()
        self.createMenu()

        self.CONNECT_SIGNAL.connect(self.clientConnectHandle)
        self.DISCONNECT_SIGNAL.connect(self.clientDisconnectHandle)
        self.GET_FTP_SIGNAL.connect(self.getFTPInfoHandle)
        self.JOB_UPDATE_SIGNAL.connect(self.updateJobHandle)
        self.GET_SOFT_VERSION_SIGNAL.connect(self.getSoftVersionHandle)
        self.GET_ERROR_SIGNAL.connect(self.getErrorHandle)
        self.GET_FILE_VALID_SIGNAL.connect(self.getFileValidHandle)
        self.PAY_R_SIGNAL.connect(self.payRequestHandle)

        self.SUBMIT_SIGNAL.connect(self.submitTaskHandle)
        self.JOB_SUBMIT_SIGNAL.connect(self.jobSubmitTaskHandle)
        self.UPDATE_SIGNAL.connect(self.updateTaskHandle)
        self.CANCEL_SIGNAL.connect(self.cancelTaskHandle)
        self.FINISH_SIGNAL.connect(self.finishTaskHandle)
        self.CS_UPDATE_SIGNAL.connect(self.cs_updateHandle)

    def initUI(self):
        self.tableLayout = self.findChild(QtGui.QLayout, "treeLayout")
        self.table_widget = UserTable()
        self.tableLayout.addWidget(self.table_widget)

        # ========== Test Button ============
        testBtn = self.findChild(QtGui.QPushButton, "TestBtn")
        testBtn.clicked.connect(self.testHandle)
        test2Btn = self.findChild(QtGui.QPushButton, "Test2Btn")
        test2Btn.clicked.connect(self.test2Handle)
        testBtn.hide()
        test2Btn.hide()
        # ========== Test Button ============

        # Menu #######################
        manage_user = self.findChild(QtGui.QAction, "actionManage_User")
        manage_user.activated.connect(self.manageUserHandle)

        manage_config = self.findChild(QtGui.QAction, "actionManage_Configure")
        manage_config.activated.connect(self.manageConfigHandle)

        exit_menu = self.findChild(QtGui.QAction, "action_Exit")
        exit_menu.activated.connect(self.close)

        readme = self.findChild(QtGui.QAction, "actionFFM_RMM")
        readmeIcon = os.path.join(os.path.dirname(__file__), os.pardir, FILE.ICON_HELP)
        readme.setIcon(QtGui.QIcon(readmeIcon))
        readme.triggered.connect(self.readme)

        about = self.findChild(QtGui.QAction, "actionAbout")
        aboutIcon = os.path.join(os.path.dirname(__file__), os.pardir, FILE.ICON_INFO)
        about.setIcon(QtGui.QIcon(aboutIcon))
        about.triggered.connect(self.about)
        # #############################

    def createMenu(self):
        self.fileMenu = QtGui.QMenu(self)

        showUserInfoMenu = self.fileMenu.addAction("Show User Information")
        showUserInfoMenu.triggered.connect(self.showUserInfoHandle)

        showJobsMenu = self.fileMenu.addAction("Show Jobs")
        showJobsMenu.triggered.connect(self.showJobsHandle)

        self.fileMenu.addSeparator()

        openRootPathMenu = self.fileMenu.addAction("Open Root Path")
        openRootPathMenu.triggered.connect(self.openRootPath)

        self.fileMenu.addSeparator()

        updateMenu = self.fileMenu.addAction("Update")
        updateMenu.setShortcut("F5")
        updateMenu.triggered.connect(self.updateUserInfo)

        # Add menu to panel.
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(
            lambda: self.fileMenu.exec_(QtGui.QCursor.pos()))

        shotcut_update = QtGui.QShortcut(QtGui.QKeySequence("F5"), self)
        shotcut_update.activated.connect(self.updateUserInfo)

    def updateUserInfo(self):
        # print "updateUserInfo"
        while self.table_widget.rowCount() > 0:
            self.table_widget.removeRow(0)

        for rc in connect.clients.get_rc_all():
            self.table_widget.insertUser(rc)

    def showUserInfoHandle(self):
        row = self.table_widget.selectRow
        if row >= 0:
            item = self.table_widget.selectedItems()[self.table_widget.HEAD["Name"]]
            username = item.text()
            userClient = connect.clients.get_rc(username)
            editUserDg = EditUserDg(user=userClient, parent=self)

            if editUserDg.exec_():
                editUserDg.save()

    def showJobsHandle(self):
        row = self.table_widget.selectRow
        if row >= 0:
            self.table_widget.doubleClickHandle(row, 0)

    def openRootPath(self):
        # print "openRootPath"
        row = self.table_widget.selectRow
        if row >= 0:
            column = self.table_widget.HEAD["Name"]
            username = self.table_widget.item(row, column).text()
            user_client = connect.clients.get_rc(username)
            handle.showExplorer(os.path.join(user_client.root_path, "upload"))

    def clientConnectHandle(self, data):
        # print "clientConnectHandle"
        username = data.get(PARAM.NAME)
        user_client = connect.clients.get_rc(username)
        user_socket = connect.clients.get_s(username)

        try:
            if user_client:
                if user_client.checkLogin(data):
                    connect.sendMessageByName(username,
                                              protocol.MessageType.welcome,
                                              u"Welcome FFM Render Farm"
                                              )

                    connect.sendMessageByName(username,
                                              protocol.MessageType.user_info,
                                              user_client.getUserInfo
                                              )

                    # update user info
                    login_time = handle.getUTCDate()
                    user_client.last_login_time = login_time
                    user_client.ip = data[PARAM.IP]
                    user_client.saveInfo()

                    # Show User and Job on interface
                    self.table_widget.insertUser(user_client)

                    return

                else:
                    connect.sendMessageByName(username,
                                              protocol.MessageType.declined,
                                              u'The password you entered is incorrect, please try again.'
                                              )
        except Exception as e:
            util.JLOG.error("User: %s, an error occurred when connect, %s" % (username, e))

        # Any problem, disconnect.
        connect.sendMessageByName(username,
                                  protocol.MessageType.declined,
                                  'The account information is incorrect, Server'
                                  ' refuses to login.\nIf you has any question,'
                                  ' please connect administrator.'
                                  )
        user_socket.on_close()

    def clientDisconnectHandle(self, data):
        # print "clientDisconnectHandle"
        username = data[PARAM.NAME]
        item = self.table_widget.getItem(username)
        if item:
            self.table_widget.removeRow(item.row())

        # update user info
        md = MangoDBHandle()
        info = md.getUserInfo(username)

        last_login_time = parser.parse(info.get("LastLoginTime").__str__())
        logout_time = parser.parse(handle.getUTCDate().__str__())
        this_time = (logout_time - last_login_time).total_seconds()

        info.update({"_id": username,
                     "IP": data["IP"],
                     "LastLogoutTime": logout_time,
                     })

        md.saveUser(info)
        md.updateUserInfo(username, "TotalLoginTime", this_time)
        md.disconnect()

    def updateJobHandle(self, data):
        # print "updateJobHandle"
        username = data[PARAM.NAME]
        user_client = connect.clients.get_rc(username)
        user_client.initInfo()
        self.table_widget.updateInfo(user_client)
        # send job list to client
        job_list = user_client.getJobInfo()
        connect.sendMessageByName(username,
                                  protocol.MessageType.job_list,
                                  job_list
                                  )

    def getSoftVersionHandle(self, data):
        # print "getSoftVersionHandle"
        res = {'Result': 'Failed'}
        username = data[PARAM.NAME]
        soft_name = data.get("AppName")
        if not soft_name:
            return

        version_list = model.DB_CONFIGURE.getSoftwareVersion(soft_name)

        if version_list:
            res.update({'Result': 'Success',
                        'Versions': version_list
                        })
        else:
            util.JLOG.error("User: %s, get software '%s' version failed." % (username, soft_name))

        connect.sendMessageByName(username,
                                  protocol.MessageType.get_app_versions_from_server,
                                  res
                                  )

    def getErrorHandle(self, data):
        # print "getErrorHandle"
        res = {'Result': 'Failed'}
        username = data[PARAM.NAME]
        job_id = data["job_id"]
        try:
            user_client = connect.clients.get_rc(username)
            job = user_client.jobs[job_id]
            err_list = job.getErrorInfo()
            res.update({'Result': 'Success', "Errors": err_list})

        except Exception as e:
            util.JLOG.error("User: %s get error information, %s", (username, e))

        connect.sendMessageByName(username,
                                  protocol.MessageType.get_error_messages_from_server,
                                  res)

    def getFileValidHandle(self, data):
        # print "getFileValidHandle"
        cf = CheckFileMD5(data)
        cf.setDaemon(True)
        cf.start()
        # invalid_list = []
        # res = {'Result': 'Success'}
        # username = data[PARAM.NAME]
        #
        # for _file in data["FileInfo"][1:]:
        #     if os.path.exists(_file["Local"]):
        #         invalid_list.append(_file["Local"])
        #
        # if invalid_list:
        #     res = {'Result': 'Failed', 'Errors': invalid_list}
        #
        # connect.sendMessageByName(username,
        #                           protocol.MessageType.get_file_valid_from_server,
        #                           res)

    def getFTPInfoHandle(self, data):
        # print "getFTPInfoHandle"
        res = {'Result': 'Failed'}
        username = data[PARAM.NAME]
        try:
            ftp_info = model.DB_CONFIGURE.getFTP()
            res.update(ftp_info)
            res.update({
                'Result': 'Success',
                "ServerIP": DB.SERVER_LOCAL,
            })
        except Exception as e:
            util.JLOG.error("User: %s, get FTP information, %s" % (username, e))

        connect.sendMessageByName(username,
                                  protocol.MessageType.get_ftp_info_from_server,
                                  res
                                  )

    def payRequestHandle(self, data):
        # print "payRequestHandle"
        userClient = connect.clients.get_rc(data["UserName"])
        job = userClient.jobs[data["job_id"]]

        if job.pay_state:
            return

        __new_balance = userClient.total_balance - job.cost
        if __new_balance < 0:
            res = {
                u"Result": u"Failed",
                u"_id": job.id,
                u"PayState": job.pay_state,
                u"TotalBalance": userClient.total_balance,
                u"Reason": u"Not sufficient funds! Please recharge it."
            }
        elif job.state != model.STATE.Finish.value:
            res = {
                u"Result": u"Failed",
                u"_id": job.id,
                u"PayState": job.pay_state,
                u"TotalBalance": userClient.total_balance,
                u"Reason": u"Not a valid job."
            }
        else:
            job.savePayState(True)
            userClient.total_payed += job.cost
            userClient.total_balance = __new_balance
            userClient.saveInfo()
            res = {u"Result": u"Success",
                   u"_id": job.id,
                   u"PayState": job.pay_state,
                   u"TotalBalance": userClient.total_balance
                   }

        connect.sendMessageByName(userClient.username,
                                  protocol.MessageType.change_pay_state,
                                  res
                                  )

        # update user table, total pay cost
        userClient.initInfo()
        self.table_widget.updateInfo(userClient)

        # update job table if it open.
        self.updateTaskHandle(job)

    def submitTaskHandle(self, data):
        # copy file to server local from ftp.
        ch = CopyHandle(data)
        if ch.run_flag:
            t = threading.Thread(target=ch.checkHandle)
            t.setDaemon(True)
            t.start()

    def updateTaskHandle(self, job):
        # print "updateTaskHandle"
        try:
            job_item = job.client.job_window.job_table.getItem(job.id)
            if not job_item:
                return
            row = job_item.row()
            job.client.job_window.job_table.createRowItem(row, job)
        except:
            pass

    def jobSubmitTaskHandle(self, job):
        try:
            job.client.job_window.job_table.createRowItem(0, job, isNew=True)
        except:
            pass

    def cs_updateHandle(self, job_info):
        '''{u'UserName': u'jztest3', u'Progress': u'100', u'State': u'3', u'Errors': u'0', u'Job_id': u'5c91f5a9c3a4c52304c1fc80'}'''
        # print "cs_updateHandle", job_info
        job_id = job_info["Job_id"]
        username = job_info["UserName"]

        user_client = connect.clients.get_rc(username)
        if user_client:
            job = user_client.jobs[job_id]
            job.update2user(job_info)

    def cancelTaskHandle(self, data):
        # print "cancelTaskHandle"
        user_client = connect.clients.get_rc(data["UserName"])
        job = user_client.jobs[data["job_id"]]
        user_client.cancelHandle(job)

    def finishTaskHandle(self, job):
        # print "finishTaskHandle"
        job.updateInfo()

    def manageUserHandle(self):
        # print "manageUserHandle"
        mudg = ManageUserDg(self)
        mudg.exec_()
        mudg.md.disconnect()

    def manageConfigHandle(self):
        # print "manageConfigHandle"
        mcdg = ManageConfigDg(self)
        if mcdg.exec_():
            model.DB_CONFIGURE.ftpID = mcdg.FTPID
            model.DB_CONFIGURE.ftpPassword = mcdg.FTPPassword
            model.DB_CONFIGURE.ftpPath = mcdg.FTPPath
            model.DB_CONFIGURE.software = mcdg.SoftwareInfo
            model.DB_CONFIGURE.saveInfo()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, "Exit server?",
                                           "Are you sure exit server?",
                                           QtGui.QMessageBox.Yes |\
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    @staticmethod
    def readme():
        readme_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.DOC_README)
        webbrowser.open(readme_file)

    def about(self):
        contents_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.DOC_ABOUT)
        with open(contents_file, "rU") as f:
            contents = f.read()

        details_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.DOC_DETAIL)
        with open(details_file, "rU") as f:
            details = f.read()

        msg_box = QtGui.QMessageBox(self)
        msg_box.keyPressEvent = lambda event: msg_box.destroy() \
            if event.key() == QtCore.Qt.Key_Escape else None
        msg_box.setIconPixmap(QtGui.QPixmap(FILE.ICON_MAIN))
        msg_box.setWindowTitle("About FFM Render Manager Monitor")
        msg_box.setText(u"%s" % contents.decode("utf-8").replace("\n", "<br>"))
        msg_box.setDetailedText(u"%s" % details.decode("utf-8"))

        msg_box.exec_()

    def testHandle(self):
        print "testHandle"

    def test2Handle(self):
        print "test2Handle"
        from connect.deadline_connect import DLConnect

        dl = DLConnect()
        # print dl.getSlaveInfo("bcat", "IP")
        print dl.deadlineCon.Slaves.GetSlaveNames()
        print dl.deadlineCon.Slaves.GetSlaveNamesInPool("bcat")
        print dl.deadlineCon.Slaves.AddPoolToSlave("liutaichao", "bcat")
        print dl.deadlineCon.Slaves.GetSlaveNamesInPool("bcat")
        print dl.deadlineCon.Slaves.RemovePoolFromSlave("liutaichao", "bcat")
        print dl.deadlineCon.Slaves.GetSlaveNamesInPool("bcat")






def connect_server():
    t1 = ConnectThread(DB.SERVER_HOST, DB.SERVER_PORT)
    t1.setDaemon(True)
    t1.start()
    return t1


def loadConfig():
    # Create Settings.
    util.JLOG.printInfo("Config file: %s" % os.path.join(os.path.dirname(__file__), os.pardir, "config.ini"))
    config = JConfig(os.path.join(os.path.dirname(__file__), os.pardir, "config.ini"))

    DB.DEADLINE_PORT = int(config.getConfig("Server", "DEADLINE_PORT"))
    DB.DEADLINE_HOST = config.getConfig("Server", "DEADLINE_HOST")
    DB.FFM_DB_PORT = int(config.getConfig("Server", "FFM_DB_PORT"))
    DB.FFM_DB_HOST = config.getConfig("Server", "FFM_DB_HOST")

    # PC_IP = getHostIP()
    # PC_Port = 44444
    DB.SERVER_HOST = config.getConfig("Server", "SERVER_HOST")
    DB.SERVER_PORT = int(config.getConfig("Server", "SERVER_PORT"))
    DB.SERVER_LOCAL = config.getConfig("Server", "SERVER_LOCAL")

    util.JLOG.printInfo("Deadline Address: %s" % DB.DEADLINE_HOST, DB.DEADLINE_PORT)
    util.JLOG.printInfo("FFM DB Address: %s" % DB.FFM_DB_HOST, DB.FFM_DB_PORT)
    util.JLOG.printInfo("Server Address: %s" % DB.SERVER_HOST, DB.SERVER_PORT)


def run():
    handle.loadLog()
    util.JLOG.printInfo("Server START...")
    loadConfig()

    model.DB_CONFIGURE = ConfigModel()

    app = QtGui.QApplication(sys.argv)
    win = JMainWindow()
    widget.JWindow = win
    t = connect_server()

    win.show()
    sys.exit(app.exec_())


