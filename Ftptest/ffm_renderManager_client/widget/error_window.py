# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import config
import widget

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui


class ErrorWindow(QtGui.QDialog):
    def __init__(self, errors, parent=None):
        super(ErrorWindow, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowMaximizeButtonHint)

        self.setWindowTitle("Errors")
        self.setWindowIcon(QtGui.QIcon("resource/images/ffm_main.png"))

        self.error_list = QtGui.QListWidget()

        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(self.error_list)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        self.resize(720, 540)

        css_name = os.path.join(config.MAIN_PATH, 'resource/css/main.css')
        with open(css_name, 'r') as css_file:
            style_sheet = css_file.read()
        self.setStyleSheet(style_sheet)

        for error in errors:
            ui_file = os.path.join(config.MAIN_PATH, 'resource/ui/error_item.ui')

            self._widget = widget.UILoader(ui_file, css_name)
            self.frame = self._widget.findChild(QtGui.QLabel, 'label_frame')
            self.frame.setText(error['Frames'])
            self.date = self._widget.findChild(QtGui.QLabel, 'label_date')
            self.date.setText(error['Date'])
            self.content = self._widget.findChild(QtGui.QTextEdit, 'textEdit')
            self.content.setText(error['Title'])
            self.item = QtGui.QListWidgetItem()
            self.item.setSizeHint(QtCore.QSize(self._widget.size()))
            self.error_list.addItem(self.item)
            self.error_list.setItemWidget(self.item, self._widget)
