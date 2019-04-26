# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/3/4 11:53"
__all__ = ["__version__", "JobWidget"]
__version__ = "1.0.0"
import os, sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from widget.job_table import JobTable
from widget.change_pay_state_dialog import PayStateDg
from widget.error_window import ErrorWindow
from config import FILE
from util import handle
from connect import clients, protocol
import connect
import widget


class JobWidget(QtGui.QMainWindow):
    def __init__(self, username, parent=None):
        super(JobWidget, self).__init__(parent)
        self.userClient = clients.get_rc(username)
        ui_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.UI_JOB_WIDGET)
        css_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.CSS_MAIN)
        self.win = widget.UILoader(ui_file, css_file)
        self.setCentralWidget(self.win)
        self.setWindowTitle(username + "'s Jobs")
        self.resize(self.win.width(), self.win.height())
        main_icon = os.path.join(os.path.dirname((__file__)), os.pardir, FILE.ICON_MAIN)
        self.setWindowIcon(QtGui.QIcon(main_icon))

        # pay_state = self.win.findChild(QtGui.QAction, "actionChange_PayState")
        # pay_state.activated.connect(self.changePayStateHandle)

        self.tableLayout = self.findChild(QtGui.QLayout, "tableLayout")

        # create table
        self.job_table = JobTable(self.userClient)
        self.tableLayout.addWidget(self.job_table)

        self.job_table.cellDoubleClicked.connect(self.doubleClickHandle)

        # Create right menu
        self.fileMenu = QtGui.QMenu(self)

        openFolderMenu = self.fileMenu.addAction("Show in Explorer")
        openFolderMenu.triggered.connect(self.openFolderHandle)

        showErrorsMenu = self.fileMenu.addAction("Show Errors")
        showErrorsMenu.triggered.connect(self.showErrors)

        # self.fileMenu.addSeparator()

        # changePayStateMenu = self.fileMenu.addAction("Change Pay State")
        # changePayStateMenu.setShortcut("F4")
        # changePayStateMenu.triggered.connect(self.changePayStateHandle)

        # Add right menu to widget
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(
            lambda: self.fileMenu.exec_(QtGui.QCursor.pos()))

        # Add shortcut
        # shotcut_changePayState = QtGui.QShortcut(QtGui.QKeySequence("F4"), self)
        # shotcut_changePayState.activated.connect(self.changePayStateHandle)

    def doubleClickHandle(self, row, column):
        job_id = self.job_table.item(row, self.job_table.HEAD["JobID"]).text()
        jobClient = self.userClient.jobs.get(job_id)

        if not jobClient:  # Can not find job object, cancel
            return

        psdg = PayStateDg(jobClient=jobClient, parent=self)
        psdg.exec_()

    # def changePayStateHandle(self):
    #     print "changePayStateHandle"
    #     select_item = self.job_table.selectTableItem
    #     if not select_item:
    #         return
    #
    #     select_row = select_item.row()
    #     job_id = self.job_table.item(select_row, self.job_table.HEAD["JobID"]).text()
    #     jobClient = self.userClient.jobs.get(job_id)
    #
    #     if not jobClient:  # Can not find job object, cancel
    #         return
    #
    #     psdg = PayStateDg(jobClient=jobClient, parent=self)
    #     if psdg.exec_():
    #         if psdg.isPayState == jobClient.pay_state:
    #             return  # no change
    #
    #         # jobClient.pay_state = psdg.isPayState
    #         # jobClient.saveJob()
    #         jobClient.savePayState(psdg.isPayState)
    #
    #         self.job_table.createPayLabel(select_row, psdg.isPayState)
    #
    #         total_cost = self.userClient.total_payed
    #         _cost = jobClient.cost
    #
    #         if jobClient.pay_state:
    #             if not psdg.isPayState:
    #                 # state: Before payed, now unpayed, - cost, if not totalCost, do not handle.
    #                 if total_cost:
    #                     _cost = -_cost
    #                 else:
    #                     _cost = 0
    #
    #         connect.sendMessageByName(self.userClient.username,
    #                                   protocol.MessageType.change_pay_state,
    #                                   {"_id": job_id, "PayState": jobClient.pay_state}
    #                                   )

    def openFolderHandle(self):
        # print "openFolderHandle"
        select_item = self.job_table.selectTableItem
        if not select_item:
            return

        select_row = select_item.row()
        job_id = self.job_table.item(select_row, self.job_table.HEAD["JobID"]).text()
        jobClient = self.userClient.jobs.get(job_id)

        if not jobClient:  # Can not find job object, cancel
            return

        handle.showExplorer(jobClient.out_dir[0])

    def showErrors(self):
        # print "showErrors"
        select_item = self.job_table.selectTableItem
        if not select_item:
            return

        select_row = select_item.row()
        job_id = self.job_table.item(select_row, self.job_table.HEAD["JobID"]).text()
        jobClient = self.userClient.jobs.get(job_id)

        if not jobClient:  # Can not find job object, cancel
            return

        error_info = jobClient.getErrorInfo()
        if len(error_info) == 0:
            return

        error_window = ErrorWindow(error_info)
        error_window.exec_()

    def keyPressEvent(self, event):
        # print event.key()
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def close(self, *args, **kwargs):
        if self.userClient and self.userClient.job_window != None:
            self.userClient.job_window = None
        super(JobWidget, self).close(*args, **kwargs)

    def closeEvent(self, *args, **kwargs):
        if self.userClient and self.userClient.job_window != None:
            self.userClient.job_window = None
        super(JobWidget, self).closeEvent(*args, **kwargs)
