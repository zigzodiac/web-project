# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/2 16:02"
__all__ = ["__version__", "FILE", "PARAM", "PATH", "CONFIG"]
__version__ = "1.0.0"

import os



class PARAM:
    NAME = "PC-Name"
    IP = "IP"
    APPS = "APPS"


class PATH:
    ROOT = os.path.expanduser("~\\FFM")


class FILE:
    UI_MAIN_WINDOW = os.path.join("UI", "mainWindow.ui")
    UI_EDIT_CONFIG = os.path.join("UI", "editConfigure.ui")
    UI_SELECT_INSTALL_DG = os.path.join("UI", "installSelectDialog.ui")
    UI_CHANGE_CONFIG = os.path.join("UI", "changeConfigureDialog.ui")
    UI_CONFIRM = os.path.join("UI", "confirmDg.ui")
    UI_EDIT_SERVER = os.path.join("UI", "editServer.ui")
    CSS_MAIN = os.path.join("UI", "main.css")
    FILE_LOG = None
    ICON_MAIN = os.path.join("UI", "ffm_main.png")
    ICON_INFO = os.path.join("UI", "icon", "info.png")
    ICON_HELP = os.path.join("UI", "icon", "help.png")

    README = os.path.join("document", "ReadMe.html")
    INSTALL_PACKAGE_INSTRUCTION = os.path.join("document", "Installation Package Instructions.html")
    ABOUT = os.path.join("document", "about.txt")

    CONFIG = os.path.join(PATH.ROOT, "FFM RenderFarm Configure File.ini")


class CONFIG:
    SEC_SERVER = "Server"
    KEY_IP = "IP"
    KEY_PORT = "PORT"

    SEC_INSTALL = "Install"
    SEC_UNINSTALL = "Uninstall"
    SEC_PATH = "Path"