# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/1/23 16:03"
__all__ = ["__version__", "PayStateDg"]
__version__ = "1.0.0"
import os
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from config import FILE
import widget


class PayStateDg(QtGui.QDialog):
    def __init__(self, jobClient, parent=None):
        super(PayStateDg, self).__init__(parent)
        self.jobClient = jobClient

        ui_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.UI_PAY_STATE)
        css_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.CSS_MAIN)
        self.win = widget.UILoader(ui_file, css_file)
        self.setWindowTitle("Change Pay State Dialog - User: %s, Job ID: %s" \
                            % (self.jobClient.username, self.jobClient.id))
        l = self.win.findChild(QtGui.QLayout, "gridLayout")
        self.setLayout(l)
        self.setFixedSize(self.win.width(), self.win.height())
        self.setStyleSheet(self.win.styleSheet())
        main_icon = os.path.join(os.path.dirname((__file__)), os.pardir, FILE.ICON_MAIN)
        self.setWindowIcon(QtGui.QIcon(main_icon))

        self.info_table = self.findChild(QtGui.QTableWidget, "infoTable")
        self.isPayBox = self.findChild(QtGui.QCheckBox, "isPay")
        self.isPayBox.hide()

        self.isPayBox.setEnabled(False)
        if self.jobClient.pay_state:
            self.isPayBox.setCheckState(QtCore.Qt.Checked)
            # === This control pay state checkBox enable. ===
            # self.isPayBox.setEnabled(False)

        # if self.jobClient.progress != 100:
        #     self.isPayBox.setEnabled(False)

        btn_box = self.findChild(QtGui.QDialogButtonBox, "buttonBox")
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

        self.addData("Job ID", self.jobClient.id)
        self.addData("UserName", self.jobClient.username)
        self.addData("Submit Time", self.jobClient.submit_time)
        self.addData("Start Time", self.jobClient.start_time)
        self.addData("Complete Time", self.jobClient.complete_time)
        self.addData("Render Time", self.jobClient.render_time)
        self.addData("Job Cost", self.jobClient.cost)
        self.addData("Pay State", self.jobClient.pay_state)

    def addData(self, key, value):
        '''
        :param key: title, str
        :param value:  information, from jobClient
        '''
        row = self.info_table.rowCount()
        self.info_table.insertRow(row)
        key_item = QtGui.QTableWidgetItem(key)
        key_item.setToolTip(key)
        value_item = QtGui.QTableWidgetItem(value)
        value_item.setToolTip(str(value))
        self.info_table.setItem(row, 0, key_item)
        self.info_table.setItem(row, 1, value_item)

    @property
    def isPayState(self):
        return True if self.isPayBox.checkState() else False



