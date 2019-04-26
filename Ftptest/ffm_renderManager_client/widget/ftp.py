# !/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import shutil
import config
from PySide import QtGui
from PySide import QtCore
import widget

from ffm.ffm_ftp.ftp_thread import FtpThread
from ffm.ffm_ftp.progress import Progress
import threading

import zipfile


class FtpDialog(QtGui.QDialog):
    ACCEPT = QtCore.Signal()

    def __init__(self, _files, _dest_path):
        super(FtpDialog, self).__init__()

        self.is_upload = False
        if type(_files[1]) == dict:
            self.is_upload = True

        self.ACCEPT.connect(self.accept)

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowMaximizeButtonHint)

        ui_file = os.path.join(config.MAIN_PATH, 'resource/ui/ftp_uploader.ui')
        css_file = os.path.join(config.MAIN_PATH, 'resource/css/main.css')
        self.main_ui = widget.UILoader(ui_file, css_file)
        self.setWindowIcon(QtGui.QIcon("resource/images/ffm_main.png"))

        self.file_list = self.main_ui.findChild(QtGui.QListWidget, 'listWidget_file_list')

        cancel_button = self.main_ui.findChild(QtGui.QPushButton, 'pushButton_cancel')
        cancel_button.clicked.connect(self.__cancel)

        main_layout = QtGui.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.main_ui)
        self.setLayout(main_layout)

        self.ftp = FtpThread(host=widget.JWindow.ftp_ip, user=widget.JWindow.ftp_id, passwd=widget.JWindow.ftp_pw, acct='21')
        self.ftp.connectFTP()

        if self.is_upload:
            self.setWindowTitle("File Uploader")
            self.reupload_button = self.main_ui.findChild(QtGui.QPushButton, 'pushButton_reupload')
            self.reupload_button.clicked.connect(self.__reuploadFiles)
            self.reupload_button.setEnabled(False)
            self.ftp.upload_signal_fail.connect(self.uploadFaileEvent)
            # self.ftp.upload_signal_success.connect(self.uploadSuccessEvent)

            self.upload_files = _files
            self.render_output_path = _dest_path
            self.__run_uploader()
        else:
            self.setWindowTitle("File Downloader")
            self.reupload_button = self.main_ui.findChild(QtGui.QPushButton, 'pushButton_reupload')
            self.reupload_button.setText('Re Download')
            self.reupload_button.clicked.connect(self.__redownloadFiles)
            self.reupload_button.setEnabled(False)
            self.ftp.download_signal_fail.connect(self.downloadFaileEvent)
            self.ftp.download_signal_success.connect(self.downloadSuccessEvent)

            self.download_files = _files
            self.local_path = _dest_path
            self.__run_downloader()

    def __run_uploader(self):
        # Prepare Directories in FTP
        # Create Output Path in FTP
        server_path = widget.JWindow.ftp_path.replace(widget.JWindow.ftp_ip, widget.JWindow.server_ip)
        ftp_abs_path = self.render_output_path.replace(server_path + '\\', '')
        # ftp_abs_path = self.render_output_path.replace('\\\\DC01\\', '')
        ftp_path_list = ftp_abs_path.split('\\')

        print ('ftp_path_list: ', ftp_path_list)

        for ftp_path in ftp_path_list:
            dirs = self.ftp.nlst()
            if ftp_path not in dirs:
                self.ftp.mkd(ftp_path)
            self.ftp.cwd(ftp_path)

        # Create Upload Path in FTP
        self._upload_files = []
        for f in self.upload_files[1:]:
            for vaild_f in self.upload_files[0]['file']:
                if vaild_f == f['Local']:
                    local_file = f['Local']
                    ftp_file = f['Ftp'][0]

                    self._upload_files.append(local_file)

                    ftp_abs_path = ftp_file.replace(server_path + '\\', '')
                    # ftp_abs_path = ftp_file.replace('\\\\DC01\\', '')
                    ftp_path = os.path.dirname(ftp_abs_path)
                    ftp_path_list = ftp_path.split('\\')

                    print ('ftp_path_list: ', ftp_path_list)

                    self.ftp.cwd('/')

                    for ftp_path in ftp_path_list:
                        dirs = self.ftp.nlst()
                        if ftp_path not in dirs:
                            self.ftp.mkd(ftp_path)
                        self.ftp.cwd(ftp_path)

        progress = Progress()
        progress.setText(os.path.basename(self.upload_files[0]['zip']))
        progress.setValue(0)

        item = QtGui.QListWidgetItem()
        item.setData(QtCore.Qt.EditRole, os.path.basename(self.upload_files[0]['zip']))
        self.file_list.addItem(item)
        self.file_list.setItemWidget(item, progress)
        # print('%s --> %s' % (os.path.basename(self.upload_files[0]), ftp_abs_path))

        # Run Upload Thread
        self.upload_thread = threading.Thread(target=self.__upload)
        self.upload_thread.start()

        self.progress_thread = threading.Thread(target=self.__getLoadingInfo)
        self.progress_thread.start()

    def __run_downloader(self):
        for f in self.download_files:
            progress = Progress()
            progress.setText(f)
            progress.setValue(0)

            item = QtGui.QListWidgetItem()
            item.setData(QtCore.Qt.EditRole, f)
            self.file_list.addItem(item)
            self.file_list.setItemWidget(item, progress)

        # Run Download Thread
        self.download_thread = threading.Thread(target=self.__download)
        self.download_thread.start()

        self.progress_thread = threading.Thread(target=self.__getLoadingInfo)
        self.progress_thread.start()

    def __download(self):
        self.ftp.download(self.download_files, self.local_path)

    def __packFiles(self, zip_file_path, file_path_list):
        zipfiles = zipfile.ZipFile(zip_file_path, 'w', allowZip64=True)

        for file in file_path_list:
            zipfiles.write(file, os.path.basename(file), compress_type=zipfile.ZIP_DEFLATED)

        zipfiles.close()

    def __upload(self):
        up_path = '/' + widget.JWindow.user_id + '/upload'

        zip_files_path = [os.path.join(config.ZIP_CRUSH_PATH, os.path.basename(self.upload_files[0]['zip']))]

        try:
            self.__packFiles(zip_files_path[0], self._upload_files)
            self.ftp.upload(zip_files_path, up_path)
        except Exception as e:
            print('Error: ' + str(e))
            print('Error: upload is failed')

    def __getLoadingInfo(self):
        while True:
            if self.ftp.ftp.is_cancel == True:
                return

            loading_file_index = self.ftp.ftp.getLodingFileIndex()
            if loading_file_index != -1:
                loading_file = self.ftp.ftp.getLodingFile()
                loading_percent = self.ftp.ftp.getLodingPercent()

                # print loading_file, loading_file_index, loading_percent, len(loading_percent)
                cur_percent = loading_percent[loading_file_index]

                item = self.file_list.item(0)
                progress = self.file_list.itemWidget(item)
                progress.setText(loading_file)
                progress.setValue(cur_percent)

                if loading_file_index == (len(loading_percent) - 1):
                    if loading_percent[loading_file_index] >= 99.9999:
                        break
        self.ACCEPT.emit()


    def __redownloadFiles(self):
        print '__redownloadFiles'
        if self.ftp.ftp.is_cancel == False:
            return

        self.ftp = FtpThread(host=widget.JWindow.ftp_ip, user=widget.JWindow.ftp_id, passwd=widget.JWindow.ftp_pw,
                             acct='21')
        self.ftp.download_signal_fail.connect(self.downloadFaileEvent)
        # self.ftp.download_signal_success.connect(self.downloadSuccessEvent)
        self.ftp.connectFTP()

        self.download_thread = threading.Thread(target=self.__download)
        self.download_thread.start()

        self.progress_thread = threading.Thread(target=self.__getLoadingInfo)
        self.progress_thread.start()


    def __reuploadFiles(self):
        print '__reuploadFiles'
        if self.ftp.ftp.is_cancel == False:
            return

        self.ftp = FtpThread(host=widget.JWindow.ftp_ip, user=widget.JWindow.ftp_id, passwd=widget.JWindow.ftp_pw, acct='21')
        self.ftp.upload_signal_fail.connect(self.uploadFaileEvent)
        # self.ftp.upload_signal_success.connect(self.uploadSuccessEvent)
        self.ftp.connectFTP()

        self.upload_thread = threading.Thread(target=self.__upload)
        self.upload_thread.start()

        self.progress_thread = threading.Thread(target=self.__getLoadingInfo)
        self.progress_thread.start()

    def closeEvent(self, event):
        self.__cancel()

    def __cancel(self):
        print '__cancel'
        self.ftp.ftp.is_cancel = True
        self.reupload_button.setEnabled(True)

        try:
            self.ftp.wait()
        except:
            pass

    def downloadSuccessEvent(self):
        QtGui.QMessageBox.information(self, 'success', 'download is success', QtGui.QMessageBox.Yes)
        os.startfile(self.local_path)

    def downloadFaileEvent(self, error):
        self.__cancel()
        QtGui.QMessageBox.warning(self, 'download is failed', error, QtGui.QMessageBox.Yes)

    def uploadSuccessEvent(self):
        QtGui.QMessageBox.information(self, 'success', 'upload is success', QtGui.QMessageBox.Yes)
        shutil.rmtree(config.ZIP_CRUSH_PATH)
        os.mkdir(config.ZIP_CRUSH_PATH)

    def uploadFaileEvent(self, error):
        self.__cancel()
        QtGui.QMessageBox.warning(self, 'upload is failed', error, QtGui.QMessageBox.Yes)
