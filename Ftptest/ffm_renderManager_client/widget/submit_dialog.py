# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import config
import widget
import copy
import connect
from connect import protocol
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
import datetime
import pprint
from widget.ftp import FtpDialog
from ffm.file.jfile import MD5File
import util


class SubmitDialog(QtGui.QDialog):
    GET_VERSIONS_SIGNAL = QtCore.Signal(dict)
    GET_FILE_VALID_SIGNAL = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super(SubmitDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowMaximizeButtonHint)

        ui_file = os.path.join(config.MAIN_PATH, 'resource/ui/submit.ui')
        css_file = os.path.join(config.MAIN_PATH, 'resource/css/main.css')
        self.main_ui = widget.UILoader(ui_file, css_file)
        self.setWindowTitle("Submit Rendering Job")
        self.setWindowIcon(QtGui.QIcon("resource/images/ffm_main.png"))

        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(self.main_ui)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(main_layout)

        open_scene_file = self.main_ui.findChild(QtGui.QPushButton, 'pushButton_openFile')
        open_scene_file.clicked.connect(self.__openSceneFile)

        self.scene_file = self.main_ui.findChild(QtGui.QLineEdit, 'lineEdit_scene_file')

        self.file_structure = self.main_ui.findChild(QtGui.QTreeWidget, 'fileStructure')

        add_file = self.main_ui.findChild(QtGui.QPushButton, 'pushButton_addFile')
        add_file.clicked.connect(self.__addOtherFile)

        delete_file = self.main_ui.findChild(QtGui.QPushButton, 'pushButton_deleteFile')
        delete_file.clicked.connect(self.__deleteSelectedFile)

        submit = self.main_ui.findChild(QtGui.QPushButton, 'pushButton_submit')
        submit.clicked.connect(self.__submit)

        reset_version = self.main_ui.findChild(QtGui.QPushButton, 'pushButton_reset_version')
        reset_version.clicked.connect(self.__requestAppVersion)

        self.app_versions = self.main_ui.findChild(QtGui.QComboBox, 'comboBox_app_version')
        self.renderer = self.main_ui.findChild(QtGui.QComboBox, 'comboBox_renderer')

        self.start_frame = self.main_ui.findChild(QtGui.QSpinBox, 'spinBox_start')
        # self.start_frame.valueChanged.connect(self.__startFrameValueChanged)

        self.end_frame = self.main_ui.findChild(QtGui.QSpinBox, 'spinBox_end')
        # self.end_frame.valueChanged.connect(self.__endFrameValueChanged)

        self.job_name = self.main_ui.findChild(QtGui.QLineEdit, 'lineEdit_jobName')
        self.job_comment = self.main_ui.findChild(QtGui.QLineEdit, 'lineEdit_jobComment')
        self.camera = self.main_ui.findChild(QtGui.QLineEdit, 'lineEdit_camera')

        self.frame_camera = self.main_ui.findChild(QtGui.QFrame, 'frame_camera')
        self.frame_renderer = self.main_ui.findChild(QtGui.QFrame, 'frame_renderer')
        self.frame_render_node = self.main_ui.findChild(QtGui.QFrame, 'frame_renderNode')
        self.frame_render_node.hide()
        self.render_node = self.main_ui.findChild(QtGui.QLineEdit, 'lineEdit_renderNode')

        self.GET_VERSIONS_SIGNAL.connect(self.__setAppVersion)
        self.GET_FILE_VALID_SIGNAL.connect(self.__getFileValid)

        self.now_date = datetime.datetime.now()

        self._app_version = None

        self.__submit_infos = None

        # # Test
        # _test = self.main_ui.findChild(QtGui.QPushButton, 'test')
        # _test.clicked.connect(self.test)

    def setJobData(self, job_item):
        self.scene_file.setText(job_item.scene_file)

        for local_file in job_item.local_files:
            self.__addFile(local_file)

        self.job_name.setText(job_item.name)
        self.job_comment.setText(job_item.comment)

        frames = job_item.frames.split('-')
        self.start_frame.setValue(int(frames[0]))
        self.end_frame.setValue(int(frames[-1]))
        self.camera.setText(job_item.camera)

        self.render_node.setText(str(job_item.output_driver))
        self.__setRenderer()
        renderer_index = self.renderer.findText(job_item.renderer, QtCore.Qt.MatchFlag.MatchContains)
        self.renderer.setCurrentIndex(renderer_index)

        self.__requestAppVersion()
        self._app_version = job_item.version

    # def test(self):
    #     print 'test'

    def getSubmitInfos(self):
        return self.__submit_infos

    def getSubmitInfo(self):
        print 'getSubmitInfo'
        scene_file_path = self.scene_file.text()
        job_name = self.job_name.text().strip()
        job_comment = self.job_comment.text().strip()
        camera = self.camera.text().strip()

        time_str = self.now_date.strftime(protocol.MessageType.TIME_FORMAT.value)
        time_str = time_str.replace(' ', '__')
        time_str = time_str.replace(':', '-')

        server_path = widget.JWindow.ftp_path.replace(widget.JWindow.ftp_ip, widget.JWindow.server_ip)
        # server_path = widget.JWindow.ftp_path.replace(widget.JWindow.ftp_ip, 'DC01')

        ftp_path = server_path + '\\' + widget.JWindow.user_id + '\\upload'

        output_path = server_path + '\\' + widget.JWindow.user_id + '\\output\\' + time_str

        zip_file_path = ftp_path + '\\' + 'zip_' + time_str + '.zip'

        widget.NOTIFY.run('Please wait a second')
        files = [{'zip': zip_file_path, 'file': []}]
        for f in self.__getAllFiles():
            hash_code = MD5File(f)
            file_name = os.path.basename(f)
            files.append({
                'Local': f,
                'Ftp': (os.path.join(ftp_path, file_name), hash_code)
            })

        infos = {
            'JobInfo': {
                "Plugin": "MayaBatch",
                "Name": job_name,
                "Comment": job_comment,
                "Department": widget.JWindow.user_id,
                "Pool": widget.JWindow.user_id,
                # "Pool": "none",
                "Group": "none",
                "Priority": "50",
                "TaskTimeoutMinutes": "0",
                "EnableAutoTimeout": "false",
                "ConcurrentTasks": "1",
                "LimitConcurrentTasksToNumberOfCpus": "true",
                "MachineLimit": "0",
                "OnJobComplete": "Nothing",
                "Frames": str(self.start_frame.value()) + '-' + str(self.end_frame.value()),
                "ChunkSize": "1",
                "OutputDirectory0": output_path,
                'UserName': widget.JWindow.user_id
            },
            'PluginInfo': {
                "SceneFile": scene_file_path,
                "Version": self.app_versions.currentText(),
                "Build": "64bit",
                "StrictErrorChecking": "true",
                "UseLegacyRenderLayers": "false",
                "LocalRendering": "false",
                "MaxProcessors": "0",
                "FrameNumberOffset": "0",
                "UseOnlyCommandLineOptions": "false",
                "IgnoreError211": "0"
            },
            'FileInfo': files
        }

        filename_list = scene_file_path.split('.')
        filename = os.path.basename(filename_list[0])
        ext = filename_list[-1].lower()
        if ext == 'mb' or ext == 'ma':
            infos['JobInfo']['Plugin'] = 'MayaBatch'
            infos['PluginInfo']['OutputFilePath'] = output_path
            infos['PluginInfo']['Camera'] = camera
            infos['PluginInfo']['Renderer'] = self.renderer.currentText()

            if self.renderer.currentText() == 'Arnold':
                infos['PluginInfo']['ArnoldVerbose'] = '1'

        elif ext == 'hip':
            infos['JobInfo']['Plugin'] = 'Houdini'
            infos['PluginInfo']['OutputDriver'] = self.render_node.text().strip()
            infos['PluginInfo']['Output'] = output_path + '\\' + filename + '.$F4.exr'

        elif ext == 'max':
            infos['JobInfo']['Plugin'] = '3dsCmd'
            infos['PluginInfo']['Camera'] = camera
            infos['PluginInfo']['RenderOutput'] = output_path + '\\' + filename + '..exr'
            infos['PluginInfo']['GammaCorrection'] = "true"
            infos['PluginInfo']['GammaInput'] = "2.2"
            infos['PluginInfo']['GammaOutput'] = "2.2"
            infos['PluginInfo']['HiddenGeometry'] = "false"
            infos['PluginInfo']['UseAdvLighting'] = "true"
            infos['PluginInfo']['ContinueOnError'] = "true"
            infos['PluginInfo']['ComputeAdvLighting'] = "true"
            infos['PluginInfo']['RenderElements'] = "true"
            infos['PluginInfo']['IsMaxDesign'] = "false"

        elif ext == 'nk':
            infos['JobInfo']['Plugin'] = 'MayaBatch'

        elif ext == 'c4d':
            infos['JobInfo']['Plugin'] = 'MayaBatch'

        self.__submit_infos = infos
        return infos

    def __startFrameValueChanged(self, value):
        if value > self.end_frame.value():
            self.end_frame.setValue(value + 1)

    def __endFrameValueChanged(self, value):
        if value < self.start_frame.value():
            self.start_frame.setValue(value - 1)

    def __openSceneFile(self):
        print '__openSceneFile'
        old_scene_file = self.scene_file.text()
        # file_exts = '*.max *.mb *.ma *.hip *.c4d *.nk'
        file_exts = '*.max *.mb *.ma *.hip'
        file_name = QtGui.QFileDialog.getOpenFileName(None, "Select File", dir='', filter=file_exts)[0]
        if len(file_name) == 0:
            return

        file_name = file_name.replace('/', '\\')
        self.scene_file.setText(file_name)
        self.__setFileStructure(old_scene_file)
        self.__cleanupFileTree()
        self.__requestAppVersion()
        self.__setRenderer()

    def __setAppVersion(self, message):
        # print ('__setAppVersion: ' + str(message))
        self.app_versions.clear()
        if message['Result'] == 'Success':
            self.app_versions.addItems(message['Versions'])

            if self._app_version:
                version_index = self.app_versions.findText(self._app_version, QtCore.Qt.MatchFlag.MatchContains)
                self.app_versions.setCurrentIndex(version_index)

        elif message['Result'] == 'Failed':
            self.app_versions.addItem('Failed getting app versions. Please push reset button try get versions again.')

    def __requestAppVersion(self):
        file_name = self.scene_file.text()
        ext = file_name.split('.')[-1].lower()

        data = {u'UserName': widget.JWindow.user_id}

        if ext == 'mb' or ext == 'ma':
            data[u'AppName'] = 'MAYA'
        elif ext == 'hip':
            data[u'AppName'] = 'HOUDINI'
        elif ext == 'max':
            data[u'AppName'] = 'MAX'
        elif ext == 'nk':
            data[u'AppName'] = 'NUKE'
        elif ext == 'c4d':
            data[u'AppName'] = 'C4D'

        connect.Client.send_message(
            connect.packMessage(protocol.MessageType.get_app_versions.value, data)
        )

    def __setRenderer(self):
        file_name = self.scene_file.text()
        ext = file_name.split('.')[-1].lower()

        self.frame_camera.show()
        self.frame_renderer.show()
        self.frame_render_node.hide()
        self.renderer.clear()

        if ext == 'mb' or ext == 'ma':
            self.renderer.addItems(['file', 'Arnold', 'mayasoftware'])
        elif ext == 'hip':
            self.frame_renderer.hide()
            self.frame_camera.hide()
            self.frame_render_node.show()
        elif ext == 'max':
            self.frame_renderer.hide()
        elif ext == 'nk':
            self.renderer.addItems([])
        elif ext == 'c4d':
            self.renderer.addItems([])


    def __getAllFiles(self):
        all_items = self.__getAllTreeItems(self.file_structure)
        all_items.reverse()
        files = []
        for item in all_items:
            my_path = os.path.join(item.data(1, QtCore.Qt.EditRole), item.data(0, QtCore.Qt.EditRole))
            if os.path.isfile(my_path):
                files.append(my_path)
        return files


    def __cleanupFileTree(self):
        all_items = self.__getAllTreeItems(self.file_structure)
        all_items.reverse()
        for item in all_items:
            my_path = os.path.join(item.data(1, QtCore.Qt.EditRole), item.data(0, QtCore.Qt.EditRole))
            if not os.path.isfile(my_path):
                if item.childCount() == 0:
                    # print('Delete: ' + my_path)
                    self.__deleteItem(item)

    def __deleteItem(self, item):
        parent_item = item.parent()
        if not parent_item:
            model_index = self.file_structure.indexFromItem(item)
            selected_index = model_index.row()
            remove_item = self.file_structure.takeTopLevelItem(selected_index)
            del remove_item
        else:
            parent_item.removeChild(item)

    def __deleteSelectedFile(self):
        if len(self.file_structure.selectedItems()) == 0:
            return None

        selected_item = self.file_structure.selectedItems()[0]

        # If selected file is Scene file cant delete
        scene_file_path = self.scene_file.text().replace('/', '\\')
        sub_items = self.__getSubtreeItems(selected_item)
        sub_items.reverse()
        print sub_items
        for item in sub_items:
            _path = item.data(0, QtCore.Qt.EditRole)
            _parent_path = item.data(1, QtCore.Qt.EditRole)
            item_path = os.path.join(_parent_path, _path)
            if item_path == scene_file_path:
                confirm_dlg = QtGui.QDialog(self)
                css_name = os.path.join(config.MAIN_PATH, 'resource/css/main.css')
                with open(css_name, 'r') as css_file:
                    style_sheet = css_file.read()
                confirm_dlg.setStyleSheet(style_sheet)

                confirm_dlg.setWindowTitle('Delete Confirm')
                button_box = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
                button_box.accepted.connect(confirm_dlg.accept)
                button_box.rejected.connect(confirm_dlg.reject)
                layout = QtGui.QVBoxLayout()
                description = QtGui.QLabel(item_path + "\nThis is Scene File. \nDo you want delete?")
                layout.addWidget(description)
                layout.addWidget(button_box)
                confirm_dlg.setLayout(layout)

                if confirm_dlg.exec_():
                    self.__deleteItem(selected_item)
                    self.__cleanupFileTree()
                    self.scene_file.setText('')
                    self.app_versions.clear()

                return

        self.__deleteItem(selected_item)
        self.__cleanupFileTree()

    def __addOtherFile(self):
        files = QtGui.QFileDialog.getOpenFileNames(None, "Select Files", dir='C:\\')[0]
        for _file in files:
            self.__addFile(_file)

    def __setFileStructure(self, old_scene_file):
        scene_file_path = self.scene_file.text()
        if len(scene_file_path) == 0:
            return

        # remove previous scene file in tree widget
        old_path_items = old_scene_file.split('\\')
        old_file_name = old_path_items[-1]
        old_parent_path = os.path.dirname(old_scene_file)

        old_parent_item = self.__findChildItem(self.file_structure, old_path_items[0])
        for old_path in old_path_items[1:]:
            old_path_item = self.__findChildItem(old_parent_item, old_path)
            _old_path = old_path_item.data(0, QtCore.Qt.EditRole)
            _old_parent_path = old_path_item.data(1, QtCore.Qt.EditRole)

            if old_parent_path == _old_parent_path and old_file_name == _old_path:
                old_parent_item.removeChild(old_path_item)
                print 'Delete : ' + old_path
            old_parent_item = old_path_item

        # Add New Scene File
        self.__addFile(scene_file_path)


    def __addFile(self, file_path):
        if file_path[0] == '\\' and file_path[1] == '\\':
            # print 'Can not add network path. Try to Mapped Drive.'
            widget.JWindow.STATUS_MESSAGE_SIGNAL.emit('You can not add network path. Try to Mapped Drive.')
            self.scene_file.setText('')
            return

        # local_drives = util.getLocalDrives()
        # file_root_drive = file_path.split('\\')[0]
        # if file_root_drive in local_drives:
        #     widget.JWindow.STATUS_MESSAGE_SIGNAL.emit(
        #         'You can not add Local File. Try add to file in the shared directory.')
        #     self.scene_file.setText('')
        #     return

        file_path = file_path.replace('\\', '/')
        path_items = file_path.split('/')
        drive = path_items[0]
        drive_item = self.__findChildItem(self.file_structure, drive)
        if not drive_item:
            drive_item = QtGui.QTreeWidgetItem()
            drive_item.setText(0, drive + '\\')
            self.file_structure.addTopLevelItem(drive_item)

        icon_file = os.path.join(config.MAIN_PATH, 'resource/images/disk.png')
        drive_item.setIcon(0, QtGui.QIcon(icon_file))

        parent_item = drive_item
        parent_item.setData(1, QtCore.Qt.EditRole, '')
        for path in path_items[1:]:
            path_item = self.__findChildItem(parent_item, path)
            if not path_item:
                path_item = QtGui.QTreeWidgetItem()
                path_item.setData(0, QtCore.Qt.EditRole, path)

                parent_path = os.path.join(parent_item.data(1, QtCore.Qt.EditRole),
                                           parent_item.data(0, QtCore.Qt.EditRole))

                path_item.setData(1, QtCore.Qt.EditRole, parent_path)

                current_path = os.path.join(path_item.data(1, QtCore.Qt.EditRole),
                                            path_item.data(0, QtCore.Qt.EditRole))

                if os.path.isfile(current_path):
                    ext = current_path.split('.')[-1].lower()
                    if ext == 'mb':
                        icon_file = os.path.join(config.MAIN_PATH, 'resource/images/maya_mb.png')
                    elif ext == 'ma':
                        icon_file = os.path.join(config.MAIN_PATH, 'resource/images/maya_ma.png')
                    elif ext == 'hip':
                        icon_file = os.path.join(config.MAIN_PATH, 'resource/images/houdini.png')
                    elif ext == 'max':
                        icon_file = os.path.join(config.MAIN_PATH, 'resource/images/max.png')
                    else:
                        icon_file = os.path.join(config.MAIN_PATH, 'resource/images/unknown_file.png')
                else:
                    icon_file = os.path.join(config.MAIN_PATH, 'resource/images/folder_closed.png')
                path_item.setIcon(0, QtGui.QIcon(icon_file))

                parent_item.addChild(path_item)
                parent_item.setExpanded(True)
            parent_item = path_item

    def __findChildItem(self, parentItem, name):
        if type(parentItem) is QtGui.QTreeWidget:
            for i in range(parentItem.topLevelItemCount()):
                _item = parentItem.topLevelItem(i)
                if _item.text(0).find(name) != -1:
                    return _item
        else:
            for i in range(parentItem.childCount()):
                _item = parentItem.child(i)
                if _item.text(0).lower() == name.lower():
                    return _item
        return None

    def __getSubtreeItems(self, tree_item):
        items = []
        items.append(tree_item)
        for i in range(tree_item.childCount()):
            items.extend(self.__getSubtreeItems(tree_item.child(i)))
        return items

    def __getAllTreeItems(self, tree_widget):
        all_items = []
        for i in range(tree_widget.topLevelItemCount()):
            top_item = tree_widget.topLevelItem(i)
            all_items.extend(self.__getSubtreeItems(top_item))
        return all_items

    def __uploadFtp(self):
        infos = self.getSubmitInfos()

        if len(infos['FileInfo']) == 1:
            widget.NOTIFY.run('Please input the correct file name.')
            return False

        self.ftp_dlg = FtpDialog(infos['FileInfo'], infos['JobInfo']['OutputDirectory0'])

        if self.ftp_dlg.exec_():
            print '__uploadFtp: Finish!'
            return True
        return False

    def __submit(self):
        scene_file_path = self.scene_file.text()
        ext = scene_file_path.split('.')[-1].lower()
        if len(scene_file_path) == 0:
            widget.JWindow.STATUS_MESSAGE_SIGNAL.emit('Please Select Scene File.')
            return

        job_name = self.job_name.text().strip()
        if len(job_name) == 0:
            widget.JWindow.STATUS_MESSAGE_SIGNAL.emit('Please Enter Job Name.')
            return

        job_comment = self.job_comment.text().strip()
        if len(job_comment) == 0:
            widget.JWindow.STATUS_MESSAGE_SIGNAL.emit('Please Enter Job Comment.')
            return

        if ext != 'hip':
            camera = self.camera.text().strip()
            if len(camera) == 0:
                widget.JWindow.STATUS_MESSAGE_SIGNAL.emit('Please Enter Camera Name.')
                return

            if ext == 'max' and camera == 'Perspective':
                widget.JWindow.STATUS_MESSAGE_SIGNAL.emit('You can\'t select "Perspective" Camera. '
                                                          'Please select another camera.')
                return

        app_version = self.app_versions.currentText()
        if len(app_version) == 0:
            widget.JWindow.STATUS_MESSAGE_SIGNAL.emit('Please Select Version.')
            return

        # prepare upload files / check the files exist in server
        self.getSubmitInfo()
        infos = self.getSubmitInfos()
        connect.Client.send_message(
            connect.packMessage(protocol.MessageType.get_file_valid.value,
                                {"UserName": widget.JWindow.user_id, 'FileInfo': infos['FileInfo']})
        )

    def __getFileValid(self, message):

        print message, '........................................'

        if message['Result'] == 'Success':
            file_infos = self.getSubmitInfos()['FileInfo']
            files = file_infos[1:]
            repeat_files = message['Repeat']

            for file in files:
                self.repeat_flag = True
                for repeat_file in repeat_files:
                    if repeat_file == file['Local']:
                        self.repeat_flag = False
                        break

                if self.repeat_flag:
                    file_infos[0]['file'].append(file['Local'])

            res = self.__uploadFtp()
            if res:
                self.accept()
        else:
            error_files = 'Submit Failed! This files already exist in RenderFarm Server. ' \
                          'Please rename your files try upload again.\n\n'

            for f in message['Errors']:
                error_files += '\t' + f + '\n'

            widget.NOTIFY.ok_button.show()
            widget.NOTIFY.run(error_files)

