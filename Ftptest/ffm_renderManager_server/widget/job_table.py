# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/3/5 11:54"
__all__ = ["__version__", "JobTable"]
__version__ = "1.0.0"

import os, sys
from collections import OrderedDict
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from util import handle
from config import FILE


class JobTable(QtGui.QTableWidget):
    HEAD = OrderedDict([
        ("JobID", 0),
        ("JobName", 1),
        ("Comment", 2),
        ("JobState", 3),
        ("Errors", 4),
        ("Progress", 5),
        ("SubmitTime", 6),
        ("StartTime", 7),
        ("EndTime", 8),
        ("RenderTime", 9),
        ("Cost", 10),
        ("PayState", 11),
    ])

    def __init__(self, userClient, parent=None):
        super(JobTable, self).__init__(parent)
        self.setColumnCount(len(self.HEAD))
        self.setHorizontalHeaderLabels(self.HEAD.keys())
        self.setEditTriggers(self.NoEditTriggers)  # edit disable
        self.setSelectionBehavior(self.SelectRows)  # row select mode

        self.setColumnWidth(self.HEAD["JobID"], 200)
        self.setColumnWidth(self.HEAD["JobName"], 100)
        self.setColumnWidth(self.HEAD["Comment"], 100)
        self.setColumnWidth(self.HEAD["JobState"], 70)
        self.setColumnWidth(self.HEAD["Errors"], 50)
        self.setColumnWidth(self.HEAD["Progress"], 70)
        self.setColumnWidth(self.HEAD["SubmitTime"], 150)
        self.setColumnWidth(self.HEAD["StartTime"], 150)
        self.setColumnWidth(self.HEAD["EndTime"], 150)
        self.setColumnWidth(self.HEAD["RenderTime"], 100)
        self.setColumnWidth(self.HEAD["Cost"], 70)
        self.setColumnWidth(self.HEAD["PayState"], 70)

        self.userClient = userClient
        self.loadJobInfo()

    def loadJobInfo(self):
        for row, job in enumerate(self.userClient.jobs.values()):
            self.insertRow(row)
            self.createRowItem(row, job, isNew=True)

        self.sortItems(self.HEAD["SubmitTime"], QtCore.Qt.DescendingOrder)

    def createRowItem(self, row, job, isNew=False):
        if isNew == False:
            self.removeRow(row)
            self.insertRow(row)

        jobItem = QtGui.QTableWidgetItem(job.id)
        self.setItem(row, self.HEAD["JobID"], jobItem)

        name_item = QtGui.QTableWidgetItem(job.job_name)
        self.setItem(row, self.HEAD["JobName"], name_item)
        self.setJobIcon(name_item, job)
        comment_item = QtGui.QTableWidgetItem(job.comment)
        self.setItem(row, self.HEAD["Comment"], comment_item)

        # Create state label
        self.createStateLabel(row, job.state)

        # Create errors count label
        self.createErrorsLabel(row, job.errors)

        # Create progress label
        self.createProgressWidget(row, job.progress)

        # Create time item
        try:
            local_submit_time = handle.getLocalDate(job.submit_time)
            submit_time = local_submit_time.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            submit_time = ''
        self.submit_item = QtGui.QTableWidgetItem(submit_time)
        self.setItem(row, self.HEAD["SubmitTime"], self.submit_item)

        try:
            local_start_time = handle.getLocalDate(job.start_time)
            start_time = local_start_time.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            start_time = ''
        self.start_item = QtGui.QTableWidgetItem(start_time)
        self.setItem(row, self.HEAD["StartTime"], self.start_item)

        try:
            local_complete_time = handle.getLocalDate(job.complete_time)
            complete_time = local_complete_time.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            complete_time = ''
        self.complete_item = QtGui.QTableWidgetItem(complete_time)
        self.setItem(row, self.HEAD["EndTime"], self.complete_item)

        render_time_item = QtGui.QTableWidgetItem(handle.formatTime(job.render_time))
        self.setItem(row, self.HEAD["RenderTime"], render_time_item)

        # Create cost label
        cost_text = handle.formatMoney(job.cost)
        cost_item = QtGui.QTableWidgetItem(cost_text)
        cost_item.setForeground(QtGui.QBrush(QtGui.QColor(238, 238, 0, 200)))
        self.setItem(row, self.HEAD["Cost"], cost_item)

        # Create pay state label
        self.createPayLabel(row, job.pay_state)

    def createPayLabel(self, row, state):
        if state:
            pay_text = "Yes"
            pay_state_label = QtGui.QLabel(pay_text)
            pay_state_label.setObjectName("Payed")
        else:
            pay_text = "No"
            pay_state_label = QtGui.QLabel(pay_text)
            pay_state_label.setObjectName("NotPayed")
        self.setCellWidget(row, self.HEAD["PayState"], pay_state_label)

    def createStateLabel(self, row, state):
        if state == 1:
            state_label = QtGui.QLabel("Start")
            state_label.setObjectName("JobStateStart")
        elif state == 2:
            state_label = QtGui.QLabel("Queue")
            state_label.setObjectName("JobStateQueue")
        elif state == 3:
            state_label = QtGui.QLabel("Finish")
            state_label.setObjectName("JobStateFinish")
        elif state == 4:
            state_label = QtGui.QLabel("Error")
            state_label.setObjectName("JobStateError")
        else:
            state_label = QtGui.QLabel("Other")
            state_label.setObjectName("JobStateOther")
        self.setCellWidget(row, self.HEAD["JobState"], state_label)

    def createErrorsLabel(self, row, errors):
        err_count = errors
        if err_count > 0:
            errors_label = QtGui.QLabel(str(err_count))
            errors_label.setObjectName("JobError")
            self.setCellWidget(row, self.HEAD["Errors"], errors_label)

    def createProgressWidget(self, row, progress):
        self.task_progress = QtGui.QProgressBar(self)
        self.task_progress.setObjectName('task_progress')
        self.task_progress.setAlignment(QtCore.Qt.AlignCenter)
        if isinstance(progress, int):
            self.task_progress.setValue(progress)
        else:
            self.task_progress.setValue(0)
        self.setCellWidget(row, self.HEAD["Progress"], self.task_progress)

    def setJobIcon(self, jobItem, job):
        MAIN_PATH = os.path.dirname(__file__)
        ext = job.scene_file.split('.')[-1].lower()

        if ext == 'ma' or ext == 'c4d':
            icon_file = os.path.join(MAIN_PATH, os.pardir, FILE.ICON_MAYA_MA)
        elif ext == 'mb':
            icon_file = os.path.join(MAIN_PATH, os.pardir, FILE.ICON_MAYA_MB)
        elif ext == 'hip':
            icon_file = os.path.join(MAIN_PATH, os.pardir, FILE.ICON_HOUDINI)
        elif ext == 'max':
            icon_file = os.path.join(MAIN_PATH, os.pardir, FILE.ICON_MAX)
        elif ext == 'nk':
            icon_file = os.path.join(MAIN_PATH, os.pardir, FILE.ICON_NUKE)

        jobItem.setIcon(QtGui.QIcon(icon_file))

    def getItem(self, job_id):
        '''get table item by job id, if not item, return none'''
        item = self.findItems(job_id, QtCore.Qt.MatchFixedString)
        if item:
            return item[0]
        return None

    @property
    def selectTableItem(self):
        items = self.selectedItems()
        if items:
            return items[0]
