# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/1/2 16:02"
__all__ = ["__version__", "FILE", "PARAM", "PATH", "CONFIG"]
__version__ = "1.0.0"

import os


class DB:
    FFM_DB_HOST = None
    FFM_DB_PORT = None

    DEADLINE_HOST = None
    DEADLINE_PORT = None

    SERVER_HOST = None
    SERVER_PORT = None
    SERVER_LOCAL = None


class PARAM:
    NAME = "UserName"
    IP = "IP"
    ADMIN_LIST = [
        "administrator",
        "administrators",
        "admin",
        "root",
        "superuser",
        "super",
        "superman",
    ]


class PATH:
    ROOT = os.path.expanduser("~\\FFM")


class FILE:
    UI_MAIN_WINDOW = os.path.join("Resource", "ui", "mainWindow.ui")
    UI_MANAGE_USER = os.path.join("Resource", "ui", "manageUserDialog.ui")
    UI_EDIT_USER_DG = os.path.join("Resource", "ui", "editUserInfoDg.ui")
    UI_PAY_STATE = os.path.join("Resource", "ui", "payStateDg.ui")
    UI_MANAGE_CONFIG = os.path.join("Resource", "ui", "manageConfig.ui")
    UI_ADD_SOFT_DG = os.path.join("Resource", "ui", "addSoftDg.ui")
    UI_JOB_WIDGET = os.path.join("Resource", "ui", "jobWidget.ui")
    UI_ERROR_ITEM = os.path.join("Resource", "ui", "error_item.ui")
    UI_RECHARGE = os.path.join("Resource", "ui", "rechargeDg.ui")
    UI_RECHARGE_HISTORY = os.path.join("Resource", "ui", "rechargeHistoryDg.ui")

    CSS_MAIN = os.path.join("Resource", "css", "main.css")
    CSS_RECHARGE = os.path.join("Resource", "css", "recharge.css")

    ICON_MAIN = os.path.join("Resource", "icon", "ffm_main.png")
    ICON_INFO = os.path.join("Resource", "icon", "info.png")
    ICON_HELP = os.path.join("Resource", "icon", "help.png")
    ICON_MAX = os.path.join("Resource", "icon", "max.png")
    ICON_HOUDINI = os.path.join("Resource", "icon", "houdini.png")
    ICON_NUKE = os.path.join("Resource", "icon", "nuke.png")
    ICON_PS = os.path.join("Resource", "icon", "ps.png")
    ICON_MAYA_MA = os.path.join("Resource", "icon", "maya_ma.png")
    ICON_MAYA_MB = os.path.join("Resource", "icon", "maya_mb.png")
    DOC_README = os.path.join("Resource", "doc", "ReadMe.html")
    DOC_ABOUT = os.path.join("Resource", "doc", "about.txt")
    DOC_DETAIL = os.path.join("Resource", "doc", "detail.txt")

    FILE_LOG = os.path.join(PATH.ROOT, "FFM Render Manager Log.log")
    CONFIG = os.path.join(PATH.ROOT, "FFM Render Manager Configure File.ini")


class CONFIG:
    SEC_SERVER = "Server"
    KEY_IP = "IP"
    KEY_PORT = "PORT"

    SEC_INSTALL = "Install"
    SEC_UNINSTALL = "Uninstall"
    SEC_PATH = "Path"