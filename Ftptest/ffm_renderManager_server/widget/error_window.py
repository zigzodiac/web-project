# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import widget
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui

from config import FILE


class ErrorWindow(QtGui.QDialog):
    def __init__(self, errors, parent=None):
        super(ErrorWindow, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowMaximizeButtonHint)

        self.setWindowTitle("Errors")
        main_icon = os.path.join(os.path.dirname((__file__)), os.pardir, FILE.ICON_MAIN)
        self.setWindowIcon(QtGui.QIcon(main_icon))

        self.error_list = QtGui.QListWidget()

        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(self.error_list)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        self.resize(720, 540)

        css_name = os.path.join(os.path.dirname((__file__)), os.pardir, FILE.CSS_MAIN)
        with open(css_name, 'r') as css_file:
            style_sheet = css_file.read()
        self.setStyleSheet(style_sheet)

        for error in errors:
            ui_file = os.path.join(os.path.dirname((__file__)), os.pardir, FILE.UI_ERROR_ITEM)

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
