# !/usr/bin/env python
# -*- coding:utf-8 -*-

import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
from connect import protocol
from util.timer import get_localdate, formatTime
import datetime
from dateutil import parser
import widget
import model
import os
import config


class RenderJob(QtGui.QTreeWidgetItem):
    def __init__(self, _data=None):
        super(RenderJob, self).__init__()
        self.name = None
        self.id = None
        self.comment = None
        self.errors = 0
        self.errors_label = QtGui.QLabel(widget.JWindow.job_list)
        self.errors_label.setObjectName('NoErrors')

        self.task_progress = QtGui.QProgressBar(widget.JWindow.job_list)
        self.task_progress.setObjectName('task_progress')
        self.task_progress.setAlignment(QtCore.Qt.AlignCenter)
        self.task_progress.setValue(0)

        self.state = protocol.MessageType.render_submit.value
        self.frames = None
        self.submit_date = None
        self.render_start_time = None
        self.render_finish_time = None
        self.render_time_str = None
        self.render_time = None
        self.cost = None
        self.pay_state = None
        self.cost_label = QtGui.QLabel(widget.JWindow.job_list)
        self.cost_label.setObjectName('cost_item')

        self.job_state_label = QtGui.QLabel(widget.JWindow.job_list)
        self.job_state_label.setObjectName('RenderComplete')

        self.scene_file = None
        self.local_files = None
        self.version = None
        self.output_driver = None
        self.renderer = None
        self.camera = None

        self.out_dir = None
        self.tasks = None

        if _data:
            self.__initializeData(_data)
            self.__setItemData()

    def __initializeData(self, _data):
        self.name = _data['Props']['Name']
        self.id = _data['_id']
        self.comment = _data['Props']['Cmmt']

        self.errors = _data['Errs']

        if _data['Stat'] == 1:
            self.state = protocol.MessageType.render_start.value
        elif _data['Stat'] == 2:
            self.state = protocol.MessageType.render_wait.value
        elif _data['Stat'] == 3:
            self.state = protocol.MessageType.render_finish.value
        elif _data['Stat'] == 4:
            self.state = protocol.MessageType.render_cancel.value

        if 'CompProgress' in _data:
            self.task_progress.setValue(int(_data['CompProgress']))

        self.frames = _data['Props']['Frames']

        if 'Camera' in _data['Props']['PlugInfo']:
            self.camera = _data['Props']['PlugInfo']['Camera']

        if 'Renderer' in _data['Props']['PlugInfo']:
            self.renderer = _data['Props']['PlugInfo']['Renderer']

        if 'OutputDriver' in _data['Props']['PlugInfo']:
            self.output_driver = _data['Props']['PlugInfo']['OutputDriver']

        self.version = _data['Props']['PlugInfo']['Version']

        local_submit_date = get_localdate(_data['Date'])
        self.submit_date = local_submit_date.strftime(protocol.MessageType.TIME_FORMAT.value)

        try:
            local_render_start_time = get_localdate(_data['DateStart'])
            self.render_start_time = local_render_start_time.strftime(protocol.MessageType.TIME_FORMAT.value)
        except ValueError as e:
            # self.render_start_time = 'Err: ' + _data['DateStart']
            self.render_start_time = ''
        try:
            local_render_finish_time = get_localdate(_data['DateComp'])
            self.render_finish_time = local_render_finish_time.strftime(protocol.MessageType.TIME_FORMAT.value)
        except ValueError as e:
            # self.render_finish_time = 'Err: ' + _data['DateComp']
            self.render_finish_time = ''

        self.out_dir = _data['OutDir'][0]

        try:
            if 'RenderTime' in _data:
                timedelta = datetime.timedelta(seconds=_data['RenderTime'])
                _date = parser.parse(str(timedelta))
                total_render_time = _date.strftime("%H:%M:%S")
                self.render_time_str = total_render_time
        except ValueError as e:
            self.render_time_str = str(timedelta)

        if 'PayState' in _data:
            self.setPayState(_data['PayState'])
        else:
            self.setPayState(False)

        if 'FileInfo' in _data:
            self.local_files = map(lambda x: x['Local'], _data['FileInfo'][1:])

        self.scene_file = _data['Props']['PlugInfo']['SceneFile']
        self.setJobIcon()

        if 'Cost' in _data:
            cost = round(_data['Cost'], 3)
            self.setJobCost(cost)

    def setJobIcon(self):
        ext = self.scene_file.split('.')[-1].lower()

        if ext == 'ma':
            icon_file = os.path.join(config.MAIN_PATH, 'resource/images/maya_ma.png')
        elif ext == 'mb':
            icon_file = os.path.join(config.MAIN_PATH, 'resource/images/maya_mb.png')
        elif ext == 'hip':
            icon_file = os.path.join(config.MAIN_PATH, 'resource/images/houdini.png')
        elif ext == 'max':
            icon_file = os.path.join(config.MAIN_PATH, 'resource/images/max.png')
        elif ext == 'nk':
            icon_file = os.path.join(config.MAIN_PATH, 'resource/images/nuke.png')
        # elif ext == 'c4d':
        #     icon_file = os.path.join(config.MAIN_PATH, 'resource/images/maya_ma.png')
        self.setIcon(0, QtGui.QIcon(icon_file))

    def setJobData(self, _data):
        self.name = _data['JobInfo']['Name']
        self.id = _data['JobInfo']['job_id']
        self.comment = _data['JobInfo']['Comment']
        self.frames = _data['JobInfo']['Frames']
        self.submit_date = _data['JobInfo']['submit_date']
        self.out_dir = _data['JobInfo']['OutputDirectory0']

        if 'FileInfo' in _data:
            self.local_files = map(lambda x: x['Local'], _data['FileInfo'][1:])

        if 'Camera' in _data['PluginInfo']:
            self.camera = _data['PluginInfo']['Camera']

        if 'Renderer' in _data['PluginInfo']:
            self.renderer = _data['PluginInfo']['Renderer']

        if 'OutputDriver' in _data['PluginInfo']:
            self.output_driver = _data['PluginInfo']['OutputDriver']

        self.version = _data['PluginInfo']['Version']
        self.scene_file = _data['PluginInfo']['SceneFile']
        self.setJobIcon()

        self.__setItemData()
        self.setPayState(False)

    def increaseErrorCount(self, count):
        if count > 0:
            self.errors_label = QtGui.QLabel(str(count), widget.JWindow.job_list)
            self.errors_label.setObjectName('Errors')
            widget.JWindow.job_list.setItemWidget(self, model.header['errors'], self.errors_label)

    def __setItemData(self):
        self.increaseErrorCount(self.errors)

        self.setJobState(self.state)

        self.setData(model.header['name'], QtCore.Qt.EditRole, self.name)
        self.setData(model.header['id'], QtCore.Qt.EditRole, self.id)
        self.setData(model.header['comment'], QtCore.Qt.EditRole, self.comment)
        self.setData(model.header['frames'], QtCore.Qt.EditRole, self.frames)
        self.setData(model.header['submit_date'], QtCore.Qt.EditRole, self.submit_date)
        self.setData(model.header['start_time'], QtCore.Qt.EditRole, self.render_start_time)
        self.setData(model.header['finish_time'], QtCore.Qt.EditRole, self.render_finish_time)
        self.setData(model.header['render_time'], QtCore.Qt.EditRole, self.render_time_str)

    def setPayState(self, _state):
        if _state:
            self.pay_state = QtGui.QLabel('Yes', widget.JWindow.job_list)
            self.pay_state.setObjectName('Payed')
        else:
            self.pay_state = QtGui.QLabel('No', widget.JWindow.job_list)
            self.pay_state.setObjectName('NotPayed')

        widget.JWindow.job_list.setItemWidget(self, model.header['payed'], self.pay_state)

    def setJobCost(self, _cost):
        self.cost = _cost
        cost_str = "{0:.2f} RMB".format(self.cost)
        self.cost_label.setText(cost_str)

    def setJobState(self, _state):
        # print 'setJobState: ', int(self.state)
        # print 'setJobState: ', self.name

        self.state = _state
        self.job_state_label = QtGui.QLabel(widget.JWindow.job_list)

        if _state == protocol.MessageType.render_submit.value:
            self.job_state_label.setText('Submitted')
            self.job_state_label.setObjectName('RenderSubmit')

        elif _state == protocol.MessageType.render_start.value:
            self.job_state_label.setText('Rendering...')
            self.job_state_label.setObjectName('RenderStart')

        elif _state == protocol.MessageType.render_progress.value:
            self.job_state_label.setText('Rendering...')
            self.job_state_label.setObjectName('RenderStart')

        elif _state == protocol.MessageType.render_wait.value:
            self.job_state_label.setText('Waiting...')
            self.job_state_label.setObjectName('RenderStart')

        elif _state == protocol.MessageType.render_cancel.value:
            self.job_state_label.setText('Canceled')
            self.job_state_label.setObjectName('RenderCancel')

        elif _state == protocol.MessageType.render_error.value:
            self.job_state_label.setText('Error')
            self.job_state_label.setObjectName('RenderError')

        elif _state == protocol.MessageType.render_finish.value:
            self.job_state_label.setText('Complete')
            self.job_state_label.setObjectName('RenderComplete')

        widget.JWindow.job_list.setItemWidget(self, model.header['job_state'], self.job_state_label)

    def updateData(self, _data):
        if 'tasks' in _data:
            self.tasks = _data['tasks']

        start_date = get_localdate(_data['DateStart'])
        end_date = get_localdate(_data['DateComp'])

        # print 'render_job : updateData : start_date', start_date
        # print 'render_job : updateData : end_date', end_date

        self.render_time = end_date - start_date

        try:
            self.render_start_time = start_date.strftime(protocol.MessageType.TIME_FORMAT.value)
            self.setData(model.header['start_time'], QtCore.Qt.EditRole, self.render_start_time)

            self.render_finish_time = end_date.strftime(protocol.MessageType.TIME_FORMAT.value)
            self.setData(model.header['finish_time'], QtCore.Qt.EditRole, self.render_finish_time)

            self.render_time_str = formatTime(_data['RenderTime'])

            self.setData(model.header['render_time'], QtCore.Qt.EditRole, self.render_time_str)

        except ValueError as e:
            self.render_time = None

        if 'job_cost' in _data:
            self.setJobCost(round(_data['job_cost'], 3))
        elif 'Cost' in _data:
            self.setJobCost(round(_data['Cost'], 3))
