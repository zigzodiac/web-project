# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/3 10:30"
__all__ = ["__version__", ]
__version__ = "1.0.0"

import PySide.QtUiTools as QtUiTools
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui

JWindow = None
NOTIFY = None

def UILoader(UI_File, css_name=None):
    '''Load UI file'''
    loader = QtUiTools.QUiLoader()   # 创建一个UILoader
    ui_file = QtCore.QFile(UI_File)  # 加载UI文件路径
    ui_file.open(QtCore.QFile.ReadOnly)   # 设置只读模式打开文件
    window = loader.load(ui_file)   # 将读取出的框架绑定到py变量
    ui_file.close()   # 关闭文件，加载成功
    if css_name:
        with open(css_name, 'r') as css_file:
            style_sheet = css_file.read()
        window.setStyleSheet(style_sheet)
    return window