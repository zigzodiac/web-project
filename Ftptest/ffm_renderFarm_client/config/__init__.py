# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
import os
import sys


__author__ = "jeremyjone"
__datetime__ = "2019/1/3 10:28"
__all__ = ["__version__", ]
__version__ = "1.0.0"


MAIN_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(MAIN_PATH)
os.chdir(MAIN_PATH)


INSTALL = 'Install'
UNINSTALL = 'Uninstall'

CONFIG_FILE = "T:/Render/renderFarmConfig.ini"
CONFIG_SERVER_SECTION = "Server"
CONFIG_PATH_SECTION = "Path"

SERVER_IP = None
SERVER_PORT = None







