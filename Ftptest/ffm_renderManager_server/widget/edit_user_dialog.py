# !/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import connect
from connect import protocol
from util import handle

__author__ = "jeremyjone"
__datetime__ = "2019/1/23 15:15"
__all__ = ["__version__", "EditUserDg"]
__version__ = "1.0.0"
import os, sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from config import FILE
from database.db_handle import MangoDBHandle
from model.client_model import RenderClient
from widget.recharge_dialog import RechargeWidget, RechargeHistoryWidget
import widget


class EditUserDg(QtGui.QDialog):
    def __init__(self, user=None, parent=None):
        super(EditUserDg, self).__init__(parent)
        ui_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.UI_EDIT_USER_DG)
        css_file = os.path.join(os.path.dirname(__file__), os.pardir, FILE.CSS_MAIN)
        self.win = widget.UILoader(ui_file, css_file)

        self.l = self.win.findChild(QtGui.QLayout, "gridLayout")
        self.setLayout(self.l)
        self.setFixedSize(self.win.width(), self.win.height())
        main_icon = os.path.join(os.path.dirname((__file__)), os.pardir, FILE.ICON_MAIN)
        self.setWindowIcon(QtGui.QIcon(main_icon))

        self.username_line = self.findChild(QtGui.QLineEdit, "usernameLine")
        username_rx = QtCore.QRegExp("^[0-9a-z_]*")
        un_Validator = QtGui.QRegExpValidator(username_rx)
        self.username_line.setValidator(un_Validator)

        self.pwd_line = self.findChild(QtGui.QLineEdit, "pwdLine")

        self.price_line = self.findChild(QtGui.QLineEdit, "priceLine")
        price_rx = QtCore.QRegExp("^(0|[1-9][0-9]*).[0-9]{2}")
        price_Validator = QtGui.QRegExpValidator(price_rx)
        self.price_line.setValidator(price_Validator)

        self.balance_line = self.findChild(QtGui.QLineEdit, "balanceLine")

        self.recharge_btn = self.findChild(QtGui.QPushButton, "RechargeBtn")
        self.recharge_btn.clicked.connect(self.rechargeHandle)
        self.history_btn = self.findChild(QtGui.QPushButton, "rechargeHistoryBtn")
        self.history_btn.clicked.connect(self.rechargeHistoryHandle)

        self.valid_box = self.findChild(QtGui.QCheckBox, "validBox")
        btn_box = self.findChild(QtGui.QDialogButtonBox, "buttonBox")
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

        self.recharge_info = None

        if user:
            self.userClient = user
            self.setWindowTitle(self.win.windowTitle() + " - " + user.username)
            self.username_line.setEnabled(False)
            username = user.username
            pwd = user.password
            price = user.unit_price
            balance = user.total_balance
            valid = QtCore.Qt.Checked if user.isvalid else QtCore.Qt.Unchecked
        else:
            self.userClient = None
            self.setWindowTitle("Add New User")
            username = pwd = ""
            price = 0.05
            balance = 0
            valid = QtCore.Qt.Checked
            self.history_btn.setEnabled(False)
            self.history_btn.setDisabled(True)
            self.history_btn.setObjectName("Btn_Disable")
            self.recharge_btn.setEnabled(False)
            self.recharge_btn.setDisabled(True)
            self.recharge_btn.setObjectName("Btn_Disable")

        self.username_line.setText(str(username))
        self.pwd_line.setText(str(pwd))
        self.price_line.setText(str(price))
        self.balance_line.setText(str(balance))
        self.valid_box.setCheckState(valid)

    @property
    def userText(self):
        return self.username_line.text()

    @property
    def pwdText(self):
        return self.pwd_line.text()

    @property
    def price(self):
        if self.price_line.text() == "":
            return 0.00
        else:
            return float(self.price_line.text())

    @property
    def validState(self):
        return True if self.valid_box.checkState() == \
                       QtCore.Qt.Checked else False

    @property
    def balance(self):
        if self.balance_line.text() == "":
            return 0.00
        else:
            return float(self.balance_line.text())

    def rechargeHandle(self):
        # print "rechargeHandle"
        rw = RechargeWidget(self.userClient, self)
        if rw.exec_():
            if rw.recharge_money == 0.00:
                # no recharge
                return

            self.balance_line.setText(str(rw.new_balance))
            date = datetime.datetime.now()  # Recharge time
            comment = rw.comment
            if comment == "":
                comment = u"Charge %s yuan at Date: %s."\
                          % (rw.recharge_money, handle.date2str(date))

            self.recharge_info = {
                u"Money": rw.recharge_money,
                u"Date": date,
                u"Comment": comment,
            }

            self.userClient.total_balance = self.balance
            if self.recharge_info:
                self.userClient.recharge_record.append(self.recharge_info)
            # print self.userClient.total_balance, self.balance

            # send new recharge record to user
            # user_info MsgTp is be easy to use, no other data needs to be modified.
            connect.sendMessageByName(self.userClient.username,
                                      protocol.MessageType.user_info,
                                      self.userClient.getUserInfo
                                      )

            self.userClient.saveInfo()

    def rechargeHistoryHandle(self):
        # print "rechargeHistoryHandle"
        rhw = RechargeHistoryWidget(self.userClient, self)
        rhw.exec_()

    def save(self):
        del_flag = False
        md = MangoDBHandle()

        if self.userClient and self.userText != self.userClient.username:
            del_flag = True
            old_name = self.userClient.username
            self.userClient = None  # change name, create new user

        if not self.userClient:  # new User
            create_time = handle.getUTCDate()
            md.saveUser({u"_id": self.userText, u"CreateDate": create_time})
            self.userClient = RenderClient(self.userText, isOnline=False)

        # save other information
        self.userClient.password = self.pwdText
        self.userClient.unit_price = self.price
        self.userClient.isvalid = self.validState

        connect.sendMessageByName(self.userClient.username,
                                  protocol.MessageType.user_info,
                                  self.userClient.getUserInfo
                                  )

        self.userClient.saveInfo()

        if del_flag:
            md.delUser(old_name)

        md.disconnect()