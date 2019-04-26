#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
author:bl
time:2019/1/8 10:56

"""


import os

if __name__ == '__main__':
    os.system('python -m PyInstaller FFM_RenderFarm_Client.spec --noconsole --icon=./resource/images/ffm_main.ico')