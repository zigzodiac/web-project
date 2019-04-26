# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
ffm render farm client start file.
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/3 10:29"
__all__ = ["__version__", ]
__version__ = "1.0.0"

import PySide.QtXml

from ffm.config.jconfig import JConfig
import config
from widget.main_widget import run


if __name__ == '__main__':

    con_local = JConfig('config.cfg')
    config.CONFIG_FILE = con_local.getConfig(config.CONFIG_PATH_SECTION, 'config_path')

    con = JConfig(config.CONFIG_FILE)
    config.SERVER_IP = con.getConfig(config.CONFIG_SERVER_SECTION, 'IP')
    config.SERVER_PORT = int(con.getConfig(config.CONFIG_SERVER_SECTION, 'PORT'))


    run((config.SERVER_IP, config.SERVER_PORT))
