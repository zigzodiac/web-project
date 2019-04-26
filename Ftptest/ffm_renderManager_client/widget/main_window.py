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
import base64
import connect
from connect.run_client import ConnectThread
from connect import protocol
import widget
from ffm.config.jconfig import JConfig
import config
from threading import Event
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
import webbrowser

from widget.submit_dialog import SubmitDialog
from widget.error_window import ErrorWindow
from widget.render_file_window import RenderFilesWindow
from widget.job_list_widget import JobList
from widget.setting_dialog import SettingDialog
from model.render_job import RenderJob
from util.timer import LogonTimerThread
import model
import datetime
from dateutil import parser
import pprint
from widget.notification import NotificationDialog

class JMainWindow(QtGui.QWidget):
    CONNECT_SIGNAL = QtCore.Signal(dict)
    INIT_SIGNAL = QtCore.Signal(dict)
    DISCONNECT_SIGNAL = QtCore.Signal(dict)
    GET_FTP_INFO_SIGNAL = QtCore.Signal(dict)
    UPDATE_JOB_LIST_SIGNAL = QtCore.Signal(dict)
    UPDATE_TIME_SIGNAL = QtCore.Signal(str)
    RENDER_SUBMIT_SIGNAL = QtCore.Signal(dict)
    RENDER_START_SIGNAL = QtCore.Signal(dict)
    RENDERPROGRESS_JOB_ITEM_SIGNAL = QtCore.Signal(dict)
    RENDER_FINISH_SIGNAL = QtCore.Signal(dict)
    RENDER_CANCEL_SIGNAL = QtCore.Signal(dict)
    RENDER_ERROR_SIGNAL = QtCore.Signal(dict)
    SHOW_ERRORS_SIGNAL = QtCore.Signal(dict)
    CHANGE_JOB_PAYMENT_SIGNAL = QtCore.Signal(dict)
    STATUS_MESSAGE_SIGNAL = QtCore.Signal(str)
    SUBMIT_RESULT_SIGNAL = QtCore.Signal(dict)

    def __init__(self):
        super(JMainWindow, self).__init__()

        self.CONNECT_SIGNAL.connect(self.__setMainWidget)
        self.INIT_SIGNAL.connect(self.__initUserInfo)
        self.DISCONNECT_SIGNAL.connect(self.__logoutEvent)
        self.GET_FTP_INFO_SIGNAL.connect(self.__setFtpPath)
        self.UPDATE_JOB_LIST_SIGNAL.connect(self.__updateJobList)
        self.UPDATE_TIME_SIGNAL.connect(self.__updateTime)
        self.RENDER_SUBMIT_SIGNAL.connect(self.__addJobItem)
        self.RENDER_START_SIGNAL.connect(self.__renderStart)
        self.RENDERPROGRESS_JOB_ITEM_SIGNAL.connect(self.__renderProgressJob)
        self.RENDER_FINISH_SIGNAL.connect(self.__renderFinish)
        self.RENDER_CANCEL_SIGNAL.connect(self.__renderCancel)
        self.RENDER_ERROR_SIGNAL.connect(self.__renderError)
        self.SHOW_ERRORS_SIGNAL.connect(self.__showErrors)
        self.CHANGE_JOB_PAYMENT_SIGNAL.connect(self.__changeJobPayment)
        self.SUBMIT_RESULT_SIGNAL.connect(self.__submitResult)

        self.resize(1280, 720)
        self.setWindowTitle("FFM Rendering Service")
        self.setWindowIcon(QtGui.QIcon("resource/images/ffm_main.png"))

        self.ftp_path = None
        self.ftp_ip = None
        self.ftp_id = None
        self.ftp_pw = None
        self.server_ip = None

        self.user_id = None
        self.user_pw = None
        self.is_login = False
        self.is_init = True
        self.client_thread = None
        self.submit_dialog = None
        self.job_list = None

        ui_file = os.path.join(config.MAIN_PATH, 'resource/ui/main_window.ui')
        css_file = os.path.join(config.MAIN_PATH, 'resource/css/main.css')
        self.window_ui = widget.UILoader(ui_file, css_file)

        self.status_bar = self.window_ui.findChild(QtGui.QStatusBar, 'statusbar')
        self.status_bar.showMessage('Please Login enter your ID or Password')
        self.STATUS_MESSAGE_SIGNAL.connect(self.status_bar.showMessage)

        action_logout = self.window_ui.findChild(QtGui.QAction, 'actionLog_Out')
        action_logout.triggered.connect(self.__logoutEvent)

        action_submit = self.window_ui.findChild(QtGui.QAction, 'actionSubmit')
        action_submit.triggered.connect(self.__submitJobEvent)

        action_resubmit = self.window_ui.findChild(QtGui.QAction, 'actionReSubmit_Job')
        action_resubmit.triggered.connect(self.__resubmitJobEvent)

        action_submit_cancel = self.window_ui.findChild(QtGui.QAction, 'actionCancelJob')
        action_submit_cancel.triggered.connect(self.__cancelJobEvent)

        action_show_render_files = self.window_ui.findChild(QtGui.QAction, 'actionShow_Render_Files')
        action_show_render_files.triggered.connect(self.__showRenderFiles)

        action_show_errors = self.window_ui.findChild(QtGui.QAction, 'actionShow_Errors')
        action_show_errors.triggered.connect(self.__showErrorsEvent)

        # action_send_error_report = self.window_ui.findChild(QtGui.QAction, 'actionSend_Error_Report')
        # action_send_error_report.triggered.connect(self.__sendErrorReport)

        action_setting = self.window_ui.findChild(QtGui.QAction, 'actionSetting')
        action_setting.triggered.connect(self.__setting)

        action_manual = self.window_ui.findChild(QtGui.QAction, 'actionManual')
        action_manual.triggered.connect(self.__manual)

        action_about = self.window_ui.findChild(QtGui.QAction, 'actionAbout')
        action_about.triggered.connect(self.__about)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(self.window_ui)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self.__setLoginWidget()

    def __updateTime(self, _time_str):
        self.logon_time.setText(_time_str)

    def __destroy(self):
        self.stopFlag.set()

    def __setFtpPath(self, message):
        if message['Result'] == 'Success':
            print ('__setFtpPath: ' + str(message))
            self.ftp_path = message['FtpPath']
            self.ftp_ip = self.ftp_path.split('\\')[2]
            self.ftp_id = message['FtpId']
            self.ftp_pw = message['FtpPw']
            self.server_ip = message['ServerIP']

        elif message['Result'] == 'Failed':
            print 'Faild to Get FTP Information'
            self.__logoutEvent()

    def closeEvent(self, event):
        self.__logoutEvent()

    def __addJobItem(self, _data):
        print '__addJobItem'
        infos = self.submit_dialog.getSubmitInfos()
        infos['JobInfo']['job_id'] = _data['job_id']

        # Need to change from server response message
        # infos['JobInfo']['submit_date'] = _data['submit_date']
        # infos['JobInfo']['submit_date'] = self.submit_dialog.now_date.strftime(protocol.MessageType.TIME_FORMAT.value)
        infos['JobInfo']['submit_date'] = _data['SubmitDate']

        job_item = RenderJob()
        job_item.setJobData(infos)
        self.job_list.insertRenderItem(job_item)

        self.submit_dialog = None

    def __submitJobEvent(self):
        if not self.is_login:
            self.STATUS_MESSAGE_SIGNAL.emit('You can use service after the login.')
            return

        # widget.NOTIFY.ok_button.show()
        # widget.NOTIFY.run('Success to Request Your Job. Please wait a moment.')
        self.submit_dialog = SubmitDialog()

        if self.submit_dialog.exec_():
            print '__submitJobEvent'
            infos = self.submit_dialog.getSubmitInfos()
            pprint.pprint(infos)
            connect.Client.send_message(
                connect.packMessage(protocol.MessageType.render_submit.value, infos)
            )

            self.STATUS_MESSAGE_SIGNAL.emit('Success to Request Submit Your Job. Please wait a moment.')
            widget.NOTIFY.run('Success to Request Submit Your Job. Please wait a moment.')
        else:
            self.submit_dialog = None
        #     self.STATUS_MESSAGE_SIGNAL.emit('Canceled submit.')

    def __submitResult(self, message):
        if message['Result'] == 'Success':
            widget.NOTIFY.closeWindow()

        elif message['Result'] == 'Failed':
            # Show the Error Files
            error_files = 'Submit Failed! This files upload failed. ' \
                          'Please try upload again or contact with administrator.\n\n'

            for f in message['ErrorFile']:
                error_files += '\t' + f + '\n'

            widget.NOTIFY.ok_button.show()
            widget.NOTIFY.run(error_files)

    def __resubmitJobEvent(self):
        if not self.is_login:
            self.STATUS_MESSAGE_SIGNAL.emit('You can use service after the login.')
            return

        if self.selectedJobItem:
            print self.selectedJobItem.name

            self.submit_dialog = SubmitDialog()
            self.submit_dialog.setJobData(self.selectedJobItem)

            if self.submit_dialog.exec_():
                print '__resubmitJobEvent'
                infos = self.submit_dialog.getSubmitInfos()
                connect.Client.send_message(
                    connect.packMessage(protocol.MessageType.render_submit.value, infos)
                )

                # self.STATUS_MESSAGE_SIGNAL.emit('Success to resubmit your Job!')
                self.STATUS_MESSAGE_SIGNAL.emit('Success to Request Resubmit Your Job. Please wait a moment.')
                widget.NOTIFY.run('Success to Request Resubmit Your Job. Please wait a moment.')
            else:
                self.submit_dialog = None

    def __changeJobPayment(self, _data):
        job_id = _data['_id']
        job_item = self.job_list.findItems(job_id, QtCore.Qt.MatchFlag.MatchContains, model.header['id'])
        if len(job_item) == 0:
            return

        if _data['Result'] == 'Success':
            pay_state = _data['PayState']
            job_item = job_item[0]

            if job_item.cost > 0:
                job_item.setPayState(pay_state)
                if pay_state:   # Yes
                    self._total_payed += job_item.cost
                    payed_cost_str = "{0:.2f} RMB".format(self._total_payed)
                    self.STATUS_MESSAGE_SIGNAL.emit('[' + job_item.name + '] This your job success to payed. '
                                                                          'You can download render files.')
                else:   # No
                    #self._total_payed -= job_item.cost
                    payed_cost_str = "{0:.2f} RMB".format(self._total_payed)
                    self.STATUS_MESSAGE_SIGNAL.emit('[' + job_item.name + '] This your job changed state to unpaid')

                my_money = _data['TotalBalance']
                totalBalance = "{0:.2f} RMB".format(my_money)
                self.my_money.setText(totalBalance)
                self.total_payed_label.setText(payed_cost_str)
        else:
            self.STATUS_MESSAGE_SIGNAL.emit(_data['Reason'])

    @property
    def selectedJobItem(self):
        if len(self.job_list.selectedItems()) == 0:
            return None
        return self.job_list.selectedItems()[0]

    def __cancelJobEvent(self):
        if not self.is_login:
            self.STATUS_MESSAGE_SIGNAL.emit('You can use service after the login.')
            return

        if self.selectedJobItem:
            if self.selectedJobItem.state == protocol.MessageType.render_start.value or\
                    self.selectedJobItem.state == protocol.MessageType.render_progress.value or \
                        self.selectedJobItem.state == protocol.MessageType.render_submit.value:
                print 'Cancel Job : ', self.selectedJobItem.name, self.selectedJobItem.id

                connect.Client.send_message(
                    connect.packMessage(
                        protocol.MessageType.render_cancel.value,
                        {"UserName": self.user_id, "job_id": self.selectedJobItem.id}
                    )
                )

    def __showRenderFiles(self):
        if not self.is_login:
            self.STATUS_MESSAGE_SIGNAL.emit('You can use service after the login.')
            return

        if self.selectedJobItem:
            self.render_file_window = RenderFilesWindow(self.selectedJobItem)
            if self.render_file_window.exec_():
                print '__showRenderFiles'


    def __showErrorsEvent(self):
        if not self.is_login:
            self.STATUS_MESSAGE_SIGNAL.emit('You can use service after the login.')
            return

        if self.selectedJobItem:
            connect.Client.send_message(
                connect.packMessage(
                    protocol.MessageType.get_error_messages.value,
                    {"UserName": self.user_id, "job_id": self.selectedJobItem.id}
                )
            )

    def __sendErrorReport(self):
        if not self.is_login:
            self.STATUS_MESSAGE_SIGNAL.emit('You can use service after the login.')
            return

        if self.selectedJobItem:
            pass

    def __payMoneyEvent(self,):
        connect.Client.send_message(
            connect.packMessage(
                protocol.MessageType.pay_request.value,
                {"UserName": self.user_id, "job_id": self.selectedJobItem.id}
            )
        )

    def __logoutEvent(self):
        if self.is_login:
            self.__setLoginWidget()
            self.is_login = False
            self.__destroy()
            self.is_init = True
        else:
            self.STATUS_MESSAGE_SIGNAL.emit('Please Login enter your ID or Password')

        if self.client_thread != None:
            if connect.Client != None:
                connect.Client.send_message(
                    connect.packMessage(
                        protocol.MessageType.disconnect.value,
                        {"UserName": self.user_id, "IP": config.SERVER_IP}
                    )
                )

                self.STATUS_MESSAGE_SIGNAL.emit('Please Login enter your ID or Password')

            self.client_thread.stop()
            self.client_thread.join()
            self.client_thread = None
            connect.Client = None

    def __loginEvent(self):
        self.user_id = self._id.text().strip()
        self.user_pw = self._pw.text().strip()

        if len(self.user_id) == 0 or len(self.user_pw) == 0:
            self.STATUS_MESSAGE_SIGNAL.emit('Something wrong. Please enter correct your ID or Password')
            return

        self.__logoutEvent()
        if self.client_thread == None:
            args = (config.SERVER_IP, config.SERVER_PORT, self.user_id, self.user_pw)
            print args
            widget.JWindow.DISCONNECT_SIGNAL.emit([])
            self.client_thread = connect_server(args)
            widget.NOTIFY.run('Please wait a moment.')

    def __setMainWidget(self, data=None):
        self.is_login = True

        main_ui_file = os.path.join(config.MAIN_PATH, 'resource/ui/mainWidget.ui')
        css_file = os.path.join(config.MAIN_PATH, 'resource/css/main.css')
        main_ui = widget.UILoader(main_ui_file, css_file)
        self.window_ui.setCentralWidget(main_ui)

        self.job_list = JobList()
        job_list_layout = self.window_ui.findChild(QtGui.QVBoxLayout, 'renderListLayout')
        job_list_layout.addWidget(self.job_list)

        action_resubmit = QtGui.QAction(self.job_list)
        action_resubmit.setText("Re Submit Job")
        action_resubmit.triggered.connect(self.__resubmitJobEvent)
        self.job_list.addAction(action_resubmit)

        action_cancel = QtGui.QAction(self.job_list)
        action_cancel.setText("Cancel Job")
        action_cancel.triggered.connect(self.__cancelJobEvent)
        self.job_list.addAction(action_cancel)

        separator = QtGui.QAction(self.job_list)
        separator.setSeparator(True)
        self.job_list.addAction(separator)

        action_show_files = QtGui.QAction(self.job_list)
        action_show_files.setText("Show Render Files")
        action_show_files.triggered.connect(self.__showRenderFiles)
        self.job_list.addAction(action_show_files)

        separator = QtGui.QAction(self.job_list)
        separator.setSeparator(True)
        self.job_list.addAction(separator)

        action_show_error = QtGui.QAction(self.job_list)
        action_show_error.setText("Show Errors")
        action_show_error.triggered.connect(self.__showErrorsEvent)
        self.job_list.addAction(action_show_error)

        action_pay_money = QtGui.QAction(self.job_list)
        action_pay_money.setText("pay money")
        action_pay_money.triggered.connect(self.__payMoneyEvent)
        self.job_list.addAction(action_pay_money)

        # action_send_error = QtGui.QAction(self.job_list)
        # action_send_error.setText("Send Error Report")
        # action_send_error.triggered.connect(self.__sendErrorReport)
        # self.job_list.addAction(action_send_error)

        self.logon_time = self.window_ui.findChild(QtGui.QLabel, 'label_logon_time')
        self.total_render_time = self.window_ui.findChild(QtGui.QLabel, 'label_total_render_time')
        self.total_payed_label = self.window_ui.findChild(QtGui.QLabel, 'label_total_payed')
        self.my_money = self.window_ui.findChild(QtGui.QLabel, 'label_myMoney')

        self._total_render_time = None
        self._total_payed = 0.0
        #self._un_payed = 0.0

        self.__startTimer()
        self.__requestFtpInfo()
        self.__requestJobUpdate()

        self.STATUS_MESSAGE_SIGNAL.emit('Hello~! ' + self.user_id + '.  Welcome to FFM Render Service!')
        widget.NOTIFY.closeWindow()

    def __requestFtpInfo(self):
        connect.Client.send_message(
            connect.packMessage(protocol.MessageType.get_ftp_info.value, {u'UserName': widget.JWindow.user_id})
        )

    def __startTimer(self):
        # Start Timer
        self.stopFlag = Event()
        self.timer_thread = LogonTimerThread(self.stopFlag, self.UPDATE_TIME_SIGNAL)
        self.timer_thread.start()

        con = JConfig(os.path.join(config.MAIN_PATH, 'renderManagerConfig.ini'))
        con.setConfig('UserInfo', 'id', self.user_id)

        comp_pw = base64.encodestring(self.user_pw)
        con.setConfig('UserInfo', 'pw', comp_pw)

    def __requestJobUpdate(self):
        connect.Client.send_message(
            connect.packMessage(protocol.MessageType.render_update.value, {u'UserName': widget.JWindow.user_id})
        )

    def __setLoginWidget(self, data=None):
        login_ui_file = os.path.join(config.MAIN_PATH, 'resource/ui/loginWidget.ui')
        css_file = os.path.join(config.MAIN_PATH, 'resource/css/main.css')
        login_ui = widget.UILoader(login_ui_file, css_file)

        self.window_ui.setCentralWidget(login_ui)

        self.login_button = self.window_ui.findChild(QtGui.QPushButton, 'pushButton_login')
        self.login_button.clicked.connect(self.__loginEvent)

        self._id = self.window_ui.findChild(QtGui.QLineEdit, 'lineEdit_id')
        self._pw = self.window_ui.findChild(QtGui.QLineEdit, 'lineEdit_pw')
        self._pw.setEchoMode(QtGui.QLineEdit.EchoMode.Password)
        self._remember_id_pw = self.window_ui.findChild(QtGui.QCheckBox, 'checkBox_remember')
        self._remember_id_pw.stateChanged.connect(self.__rememberUserInfo)

        con = JConfig(os.path.join(config.MAIN_PATH, 'renderManagerConfig.ini'))
        remember = con.getConfig('UserInfo', 'remember')

        if remember == '2':
            self._remember_id_pw.setCheckState(QtCore.Qt.CheckState.Checked)
            id = con.getConfig('UserInfo', 'id')
            pw = con.getConfig('UserInfo', 'pw')

            self._id.setText(id)

            real_pw = base64.b64decode(pw)
            self._pw.setText(real_pw)

    def __initUserInfo(self, _data):
        print '__initUserInfo'
        pprint.pprint(_data)
        self._total_payed = round(_data['TotalPayed'], 3)
        payed_cost = "{0:.2f} RMB".format(self._total_payed)
        self.total_payed_label.setText(payed_cost)

        # _cost = _data['TotalRenderCost'] - _data['TotalPayed']
        # self._un_payed = round(_cost, 3)
        # unpayed_cost = "{0:.2f} RMB".format(self._un_payed)
        # self.un_payed_label.setText(unpayed_cost)

        my_money = _data['TotalBalance']
        totalBalance = "{0:.2f} RMB".format(my_money)
        self.my_money.setText(totalBalance)

        timedelta = datetime.timedelta(seconds=_data.get('TotalRenderTime'))
        print 'timedelta: ', timedelta

        self._total_render_time = parser.parse(str(timedelta))

        print '_total_render_time: ', self._total_render_time

        total_render_time = self._total_render_time.strftime("%H:%M:%S")

        self.total_render_time.setText(total_render_time)

    def __rememberUserInfo(self, state):
        con = JConfig(os.path.join(config.MAIN_PATH, 'renderManagerConfig.ini'))

        if state == 0:
            con.setConfig('UserInfo', 'remember', '0')
        elif state == 2:
            con.setConfig('UserInfo', 'remember', '2')

    def __renderStart(self, _data):
        # pprint.pprint(_data)
        job_id = _data['job_id']
        job_item = self.job_list.findItems(job_id, QtCore.Qt.MatchFlag.MatchContains, model.header['id'])
        if len(job_item) == 0:
            return

        job_item = job_item[0]
        job_item.setJobState(protocol.MessageType.render_start.value)
        job_item.render_start_time = datetime.datetime.now().strftime(protocol.MessageType.TIME_FORMAT.value)
        job_item.setData(model.header['start_time'], QtCore.Qt.EditRole, job_item.render_start_time)

    def __renderProgressJob(self, _data):
        job_id = _data['job_id']
        job_item = self.job_list.findItems(job_id, QtCore.Qt.MatchFlag.MatchContains, model.header['id'])
        if len(job_item) == 0:
            return
        job_item = job_item[0]
        value = int(_data['complete'])
        job_item.task_progress.setValue(value)
        job_item.setJobState(protocol.MessageType.render_progress.value)
        job_item.setData(model.header['start_time'], QtCore.Qt.EditRole, _data["StartDate"])

        if value > 0:
            self.STATUS_MESSAGE_SIGNAL.emit('Rendering job [ ' + job_item.name + ' : ' + str(value) + '% ]')

    def __renderFinish(self, _data):
        job_id = _data['job_id']
        job_item = self.job_list.findItems(job_id, QtCore.Qt.MatchFlag.MatchContains, model.header['id'])
        if len(job_item) == 0:
            return

        job_item = job_item[0]
        job_item.setJobState(protocol.MessageType.render_finish.value)
        job_item.updateData(_data)
        self.finishRenderItem(job_item)

        self.STATUS_MESSAGE_SIGNAL.emit('Finish job [' + job_item.name + '].')

    def __renderCancel(self, _data):
        if _data['result'] == 'Success':
            job_id = _data['job_id']
            job_item = self.job_list.findItems(job_id, QtCore.Qt.MatchFlag.MatchContains, model.header['id'])
            if len(job_item) == 0:
                return

            job_item = job_item[0]
            job_item.setJobState(protocol.MessageType.render_cancel.value)
            job_item.task_progress.setEnabled(False)

            job_item.updateData(_data)
            self.finishRenderItem(job_item)

            self.STATUS_MESSAGE_SIGNAL.emit('Canceled job [' + job_item.name + '].')

        elif _data['result'] == 'Failed':
            self.STATUS_MESSAGE_SIGNAL.emit('Failed to Cancellation. Please try again.')

    def __renderError(self, _data):
        job_id = _data['job_id']
        job_item = self.job_list.findItems(job_id, QtCore.Qt.MatchFlag.MatchContains, model.header['id'])
        if len(job_item) == 0:
            return

        job_item = job_item[0]
        job_item.increaseErrorCount(_data['Errs'])


        job_item.setJobState(protocol.MessageType.render_error.value)
        # job_item.updateData(_data)
        # self.finishRenderItem(job_item)

        self.STATUS_MESSAGE_SIGNAL.emit('Error job [' + job_item.name + ' : ' + str(job_item.errors) + ' ].')

    def finishRenderItem(self, job_item):
        if job_item.render_time:
            total_render_time = self._total_render_time + job_item.render_time
            self.total_render_time.setText(total_render_time.strftime("%H:%M:%S"))

    def __showErrors(self, _data):
        if len(_data['Errors']) == 0:
            return

        error_window = ErrorWindow(_data['Errors'])
        if error_window.exec_():
            print '__showErrors'


    def __updateJobList(self, _data):
        if self.is_init:
            # Initialize Render Jobs
            self.is_init = False
            for job_data in _data:
                pprint.pprint(job_data)
                job_item = RenderJob(job_data)
                self.job_list.addRenderItem(job_item)

            self.job_list.sortItems(model.header['submit_date'], QtCore.Qt.DescendingOrder)

        # else:
        #     # Update
        #     self.__updateJob(_data)

    def __setting(self):
        print '__setting'

        setting_dialog = SettingDialog()

        if setting_dialog.exec_():
            print 'Setting Finish'

            con = JConfig(os.path.join(config.MAIN_PATH, 'renderManagerConfig.ini'))
            con.setConfig('Server', 'ip', setting_dialog.getIp())
            con.setConfig('Server', 'port', setting_dialog.getPort())
            config.SERVER_IP = setting_dialog.getIp()
            config.SERVER_PORT = int(setting_dialog.getPort())

    def __manual(self):
        print '__manual'
        _file = os.path.join(config.MAIN_PATH, 'document/help.md.html')
        webbrowser.open(_file)

    def __about(self):
        _file = os.path.join(config.MAIN_PATH, 'document/about.txt')

        with open(_file, "rU") as f:
            contents = f.read()

        msg_box = QtGui.QMessageBox()
        _icon = os.path.join(config.MAIN_PATH, 'resource/images/FFM_logo_wb.png')
        msg_box.setIconPixmap(QtGui.QPixmap(_icon))
        msg_box.about(self, "About FFM Rendering Service",
                      u"%s" % contents.decode("utf8").replace("\n", "<br>"))



def connect_server(args):
    t1 = ConnectThread(args)
    t1.setDaemon(True)
    t1.start()
    return t1


def run():
    app = QtGui.QApplication(sys.argv)
    win = JMainWindow()
    widget.JWindow = win
    widget.NOTIFY = NotificationDialog()
    win.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    stopFlag = Event()
    thread = LogonTimerThread(stopFlag)
    thread.start()



