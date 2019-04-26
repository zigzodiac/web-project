# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import config
import widget
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
from ffm.ffm_ftp.ftp_thread import FtpThread
from widget.ftp import FtpDialog
import util

# import connect
# from connect import protocol
# from ffm.ffm_ftp.progress import Progress
# import threading


class RenderFilesWindow(QtGui.QDialog):
    def __init__(self, job_item, parent=None):
        super(RenderFilesWindow, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint |
                            QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowMaximizeButtonHint)

        self.job_item = job_item

        ui_file = os.path.join(config.MAIN_PATH, 'resource/ui/renderFilesWindow.ui')
        css_file = os.path.join(config.MAIN_PATH, 'resource/css/main.css')
        self.main_ui = widget.UILoader(ui_file, css_file)
        self.setWindowTitle("Rendering Files")
        self.setWindowIcon(QtGui.QIcon("resource/images/ffm_main.png"))

        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(self.main_ui)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(main_layout)
        self.resize(1080, 720)

        job_name = self.main_ui.findChild(QtGui.QLabel, 'label_jobName')
        frames = self.main_ui.findChild(QtGui.QLabel, 'label_frames')
        total_render_time = self.main_ui.findChild(QtGui.QLabel, 'label_totalRenderTime')
        total_cost = self.main_ui.findChild(QtGui.QLabel, 'label_totalCost')
        payed = self.main_ui.findChild(QtGui.QLabel, 'label_payed')

        job_name.setText(self.job_item.name)
        frames.setText(self.job_item.frames)
        # total_render_time.setText(self.job_item.render_time)
        total_render_time.setText(self.job_item.render_time_str)

        total_cost.setText(self.job_item.cost_label.text())
        total_cost.setObjectName(self.job_item.cost_label.objectName())

        payed.setText(self.job_item.pay_state.text())
        payed.setObjectName(self.job_item.pay_state.objectName())

        self.check_all_items = self.main_ui.findChild(QtGui.QCheckBox, 'checkBox_selectAll')
        self.check_all_items.stateChanged.connect(self.__changeCheckState)

        self.file_structure = self.main_ui.findChild(QtGui.QTreeWidget, 'fileStructure')
        self.file_structure.setColumnWidth(0, 300)
        self.file_structure.setColumnWidth(1, 100)
        self.file_structure.setColumnWidth(2, 200)

        download = self.main_ui.findChild(QtGui.QPushButton, 'pushButton_download')
        download.clicked.connect(self.__download)

        if self.job_item.pay_state.text() == 'No':
            download.setEnabled(False)

        # self.user_ftp_path = self.job_item.out_dir.replace(widget.JWindow.ftp_path, '')
        path_list = widget.JWindow.ftp_path.split('\\')
        # path_list = self.job_item.out_dir.split('\\')
        ftp_path = '\\'.join(path_list[3:])
        self.user_ftp_path = self.job_item.out_dir.replace('\\\\' + widget.JWindow.server_ip + '\\' + ftp_path + '\\', '')
        self.user_ftp_path = self.user_ftp_path.replace('\\', '/')
        # print self.user_ftp_path

        try:
            self.__loadFiles()
        except Exception as e:
            widget.JWindow.STATUS_MESSAGE_SIGNAL.emit('Server not response. Please contact with Administrator.')
            download.setEnabled(False)

    def __changeCheckState(self, state):
        for i in range(self.file_structure.topLevelItemCount()):
            _item = self.file_structure.topLevelItem(i)
            if state == 0:
                _item.setCheckState(0, QtCore.Qt.CheckState.Unchecked)
            elif state == 2:
                _item.setCheckState(0, QtCore.Qt.CheckState.Checked)

    def __getCheckedFiles(self):
        files = []
        for i in range(self.file_structure.topLevelItemCount()):
            _item = self.file_structure.topLevelItem(i)
            if _item.checkState(0) == QtCore.Qt.CheckState.Checked:
                files.append(self.user_ftp_path + '/' + _item.text(0))
        return files

    def __loadFiles(self):
        # Need to Change this code
        # Request from server all of render task data / fileName / fileSize / renderTime / Cost

        print (widget.JWindow.ftp_ip, widget.JWindow.ftp_id, widget.JWindow.ftp_pw)

        self.ftp = FtpThread(host=widget.JWindow.ftp_ip, user=widget.JWindow.ftp_id, passwd=widget.JWindow.ftp_pw,
                             acct='21')
        self.ftp.connectFTP()

        # print self.ftp.dir()
        print self.user_ftp_path

        self.ftp.cwd(self.user_ftp_path)
        render_files = self.ftp.nlst()
        # render_files = []
        # dirs = self.ftp.dir()
        # # print dirs
        # for i in dirs:
        #     print i
        #     # itmes = i.split('  ')[-1].lstrip(' ').split(' ', 1)
        #     # render_files.append({'name': itmes[-1], 'size': int(itmes[-2])})
        print 'render_files', render_files
        for render_file in render_files:
            file_item = QtGui.QTreeWidgetItem()
            file_item.setFlags(file_item.flags() | QtCore.Qt.ItemIsUserCheckable)
            file_item.setCheckState(0, QtCore.Qt.Checked)

            # file_item.setText(0, render_file['name'])

            # print "render_file", render_file, '............................................'
            # _file_name = re.split(r"\d\d:\d\d", render_file)[1].lstrip(" ")
            # print "_file_name", _file_name, '..............................................'
            file_item.setText(0, render_file)
            # size = util.convertFileSizeFormat(render_file['size'])
            # file_item.setText(1, size)

            self.file_structure.addTopLevelItem(file_item)

        files_count = self.main_ui.findChild(QtGui.QLabel, 'label_filesCount')
        files_count.setText(str(len(render_files)) + ' items')

        # total_size = sum(map(lambda x: x['size'], render_files))
        # total_size = util.convertFileSizeFormat(total_size)

        # files_size = self.main_ui.findChild(QtGui.QLabel, 'label_filesSize')
        # files_size.setText(total_size)

    def __download(self):
        print '__download'
        down_files = self.__getCheckedFiles()
        if len(down_files) == 0:
            return

        down_path = QtGui.QFileDialog.getExistingDirectory()
        if len(down_path) == 0:
            return

        self.ftp_dlg = FtpDialog(down_files, down_path)

        if self.ftp_dlg.exec_():
            print '__downloadFtp: Finish!'
            import util
            util.openPath(down_path)
