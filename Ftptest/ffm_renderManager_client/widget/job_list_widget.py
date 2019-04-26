# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import config
import widget
import connect
from connect import protocol
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
import datetime
import pprint
import model


class JobList(QtGui.QTreeWidget):
    def __init__(self, parent=None):
        super(JobList,self).__init__(parent)
        self.setHeaderLabels(['Name', 'Comment', 'Errors', 'Progress', 'Job State', 'Frames', 'Submit Date',
                              'Start Time', 'Finish Time', 'Render Time', 'Cost', 'Payment', 'Id'])

        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.setColumnWidth(model.header['name'], 100)
        self.setColumnWidth(model.header['comment'], 90)
        self.setColumnWidth(model.header['errors'], 50)
        self.setColumnWidth(model.header['progress'], 100)
        self.setColumnWidth(model.header['job_state'], 90)
        self.setColumnWidth(model.header['frames'], 50)
        self.setColumnWidth(model.header['submit_date'], 155)
        self.setColumnWidth(model.header['start_time'], 155)
        self.setColumnWidth(model.header['finish_time'], 155)
        self.setColumnWidth(model.header['render_time'], 100)
        self.setColumnWidth(model.header['cost'], 90)

    def addRenderItem(self, render_item):
        self.addTopLevelItem(render_item)
        self.setRenderItemWidget(render_item)

    def insertRenderItem(self, render_item):
        self.insertTopLevelItem(0, render_item)
        self.setRenderItemWidget(render_item)

    def setRenderItemWidget(self, render_item):
        self.setItemWidget(render_item, model.header['progress'], render_item.task_progress)
        self.setItemWidget(render_item, model.header['errors'], render_item.errors_label)
        self.setItemWidget(render_item, model.header['job_state'], render_item.job_state_label)
        self.setItemWidget(render_item, model.header['cost'], render_item.cost_label)
        self.setItemWidget(render_item, model.header['payed'], render_item.pay_state)
