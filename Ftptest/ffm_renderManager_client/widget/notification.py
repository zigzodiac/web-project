# !/usr/bin/env python
# -*- coding:utf-8 -*-

import widget
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
import os
import config


class NotificationDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(NotificationDialog, self).__init__(parent)
        self.setObjectName('notifyWindow')
        css_name = os.path.join(config.MAIN_PATH, 'resource/css/main.css')
        with open(css_name, 'r') as css_file:
            style_sheet = css_file.read()
        self.setStyleSheet(style_sheet)

        # self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        layout = QtGui.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.__close_timer = QtCore.QTimer(self)
        self.__close_timer.timeout.connect(self.close_window)

        self.lb_message = QtGui.QTextBrowser()
        self.lb_message.setObjectName('notifyMessage')
        self.ok_button = QtGui.QPushButton('OK')
        self.ok_button.setObjectName('ConfirmButton')
        self.ok_button.clicked.connect(self.closeWindow)
        self.ok_button.hide()

        layout.addWidget(self.lb_message, 0, 0)
        layout.addWidget(self.ok_button, 1, 0)

        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.close)

    def run(self, text):
        self.__close_timer.start(5000)
        self.lb_message.setPlainText(text)

        font = self.lb_message.document().defaultFont()
        fontMetrics = QtGui.QFontMetrics(font)
        textSize = fontMetrics.size(0, text)

        textWidth = textSize.width() + 30
        textHeight = textSize.height() + 60

        self.lb_message.setMinimumSize(textWidth, textHeight)
        self.lb_message.resize(textWidth, textHeight)

        self.setMinimumSize(textWidth, textHeight)
        self.resize(textWidth, textHeight)

        x = (widget.JWindow.pos().x() + widget.JWindow.size().width() / 2) - (textWidth / 2)
        y = widget.JWindow.pos().y() + widget.JWindow.size().height() / 2
        self.move(x, y)

        if self.exec_():
            pass

    def closeWindow(self):
        self.close()

    def close_window(self):
        self.close()
        self.__close_timer.stop()
