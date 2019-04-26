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

# CONFIG_FILE = "C:/FFM/FFM_Render_Manager.ini"
CONFIG_SERVER_SECTION = "Server"
CONFIG_PATH_SECTION = "Path"

SERVER_IP = None
SERVER_PORT = None

ZIP_CRUSH_PATH = os.path.join(os.path.expanduser('~'), 'FFM_ZIP_CRUSH')
print os.path.expanduser('~')
if not os.path.exists(ZIP_CRUSH_PATH):
    os.makedirs(ZIP_CRUSH_PATH)








