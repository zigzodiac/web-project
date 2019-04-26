# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/3/22 16:17"
__all__ = ["__version__", "RechargeWidget", "RechargeHistoryWidget"]
__version__ = "1.0.0"
import os, sys
from collections import OrderedDict
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from config import FILE
from util import handle
import widget


class RechargeWidget(QtGui.QDialog):
    def __init__(self, user, parent=None):
        super(RechargeWidget, self).__init__(parent)
        self.userClient = user
        self.new_balance = self.userClient.total_balance
        self.recharge_money = 0.00

        ui_file = os.path.join(os.path.dirname(__file__), os.path.pardir, FILE.UI_RECHARGE)
        css_file = os.path.join(os.path.dirname(__file__), os.path.pardir, FILE.CSS_MAIN)
        self.win = widget.UILoader(ui_file, css_file)

        self.l = self.win.findChild(QtGui.QLayout, "gridLayout")
        self.setLayout(self.l)
        self.setFixedSize(self.win.width(), self.win.height())
        self.setWindowTitle(self.win.windowTitle())
        main_icon = os.path.join(os.path.dirname((__file__)), os.pardir, FILE.ICON_MAIN)
        self.setWindowIcon(QtGui.QIcon(main_icon))

        self.current_balance_label = self.findChild(QtGui.QLabel, "currentBalance")
        self.add_balance_label = self.findChild(QtGui.QLabel, "addBalanceLabel")

        self.comment_line = self.findChild(QtGui.QLineEdit, "commentLine")

        self.recharge_spin_box = self.findChild(QtGui.QDoubleSpinBox, "doubleSpinBox")
        self.recharge_spin_box.valueChanged.connect(self.rechargeBoxValueChangeHandle)

        btn_box = self.findChild(QtGui.QDialogButtonBox, "buttonBox")
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

        self.loadData()

    def loadData(self):
        self.current_balance_label.setText(str(self.new_balance))

    def rechargeBoxValueChangeHandle(self, data):
        cb = self.current_balance_label.text()
        self.new_balance = float(cb) + data
        self.recharge_money = data
        self.add_balance_label.setText(" + %s  =  %s" % (data, self.new_balance))

    @property
    def comment(self):
        return self.comment_line.text()


class RechargeHistoryWidget(QtGui.QDialog):
    HEAD = OrderedDict([
        ("Money", 0),
        ("Date", 1),
        ("Comment", 2),
    ])

    def __init__(self, user, parent=None):
        super(RechargeHistoryWidget, self).__init__(parent)
        self.userClient = user

        ui_file = os.path.join(os.path.dirname(__file__), os.path.pardir, FILE.UI_RECHARGE_HISTORY)
        css_file = os.path.join(os.path.dirname(__file__), os.path.pardir, FILE.CSS_MAIN)
        self.win = widget.UILoader(ui_file, css_file)

        self.l = self.win.findChild(QtGui.QLayout, "gridLayout")
        self.setLayout(self.l)
        self.resize(self.win.width(), self.win.height())
        self.setWindowTitle(self.win.windowTitle())
        main_icon = os.path.join(os.path.dirname((__file__)), os.pardir, FILE.ICON_MAIN)
        self.setWindowIcon(QtGui.QIcon(main_icon))

        self.table_widget = self.findChild(QtGui.QTableWidget, "tableWidget")
        self.table_widget.setColumnCount(len(self.HEAD))
        self.table_widget.setHorizontalHeaderLabels(self.HEAD.keys())

        # self.tree_widget = self.findChild(QtGui.QTreeWidget, "treeWidget")
        # self.tree_widget.setColumnCount(len(self.HEAD))
        # self.tree_widget.setHeaderLabels(self.HEAD.keys())

        closeBtn = self.findChild(QtGui.QPushButton, "closeBtn")
        closeBtn.clicked.connect(self.close)

        self.table_widget.setColumnWidth(self.HEAD["Date"], 180)

        self.loadData()

    def loadData(self):
        for data in self.userClient.recharge_record:
            # row = self.table_widget.rowCount()
            row = 0 # Every row insert top(0)
            self.table_widget.insertRow(row)

            money_item = QtGui.QTableWidgetItem(str(data["Money"]))
            self.table_widget.setItem(row, self.HEAD["Money"], money_item)

            date_item = QtGui.QTableWidgetItem(handle.date2str(data["Date"]))
            self.table_widget.setItem(row, self.HEAD["Date"], date_item)

            comment_item = QtGui.QTableWidgetItem(str(data.get("Comment")))
            comment_item.setToolTip(str(data.get("Comment")))
            self.table_widget.setItem(row, self.HEAD["Comment"], comment_item)

            # tree_item = QtGui.QTreeWidgetItem(
            #     # [str(data["Money"]),
            #     #  handle.date2str(data["Date"]),
            #     #  data.get("Comment")
            #     # ]
            # )
            # money_item = QtGui.QLabel(str(data["Money"]))
            # date_item = QtGui.QLabel(handle.date2str(data["Date"]))
            # print money_item.text(), date_item.text(), self.tree_widget.columnCount()
            #
            # self.tree_widget.addTopLevelItem(tree_item)
            # self.tree_widget.setItemWidget(tree_item, self.HEAD["Money"], money_item)
            # self.tree_widget.setItemWidget(tree_item, self.HEAD["Date"], date_item)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    t = RechargeWidget()
    t.show()
    sys.exit(app.exec_())
