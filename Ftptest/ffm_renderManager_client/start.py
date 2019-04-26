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
import os
from ffm.config.jconfig import JConfig
import config
from widget.main_window import run


if __name__ == '__main__':
    con = JConfig(os.path.join(config.MAIN_PATH, 'renderManagerConfig.ini'))
    try:
        config.SERVER_IP = con.getConfig(config.CONFIG_SERVER_SECTION, 'IP')
        config.SERVER_PORT = int(con.getConfig(config.CONFIG_SERVER_SECTION, 'PORT'))
    except:
       pass

    run()
