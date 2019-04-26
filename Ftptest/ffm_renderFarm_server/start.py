# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
ffm render farm server main start file.
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/2 16:03"
__all__ = ["__version__", "start"]
__version__ = "1.0.0"
import os, sys
from PySide import QtGui
from ffm.config.jconfig import JConfig

from config import FILE, CONFIG, PATH
from util.handle import getHostIP
from util.jlog import JLog, LOG_LEVEL_KEY
import util
from widget.main_widget import run
from model.config_command import Command



def start():
    app = QtGui.QApplication(sys.argv)
    PC_IP = getHostIP()
    PC_Port = 45678

    _con = JConfig(FILE.CONFIG, os.path.join(os.path.dirname(__file__),
                                             "baseConfig.ini"))
    try:
        Command.configFile = _con.getConfig("Path", "config")
        if not os.path.exists(Command.configFile):
            raise ValueError
    except:
        _file = QtGui.QFileDialog.getOpenFileName(None,
                                                  "Choose Configure File",
                                                  Command.configFile,
                                                  "Configure File (*.ini *.cfg)"
                                                  )[0]
        if not _file:
            sys.exit(0)
        _con.setConfig("Path", "config", _file)
        Command.configFile = _file

    try:
        log_path = _con.getConfig("Log", "file")
        if not os.path.exists(os.path.dirname(log_path)):
            try:
                os.makedirs(os.path.dirname(log_path))
            except:
                raise ValueError
    except:
        log_path = os.path.join(PATH.ROOT, "FFM Render Farm Log File.log")
        _con.setConfig("Log", "file", log_path)

    try:
        log_level = _con.getConfig("Log", "level")
        if log_level not in LOG_LEVEL_KEY:
            raise ValueError
    except:
        log_level = "INFO"
        _con.setConfig("Log", "level", log_level)

    try:
        log_name = _con.getConfig("Log", "name")
    except:
        log_name = "server"
        _con.setConfig("Log", "name", log_name)

    util.JLOG = JLog(log_path, log_level, log_name)
    FILE.FILE_LOG = log_path

    con = JConfig(Command.configFile)
    try:
        ip = con.getConfig(CONFIG.SEC_SERVER, CONFIG.KEY_IP)
    except:
        ip = PC_IP
        Command.config.setConfig(CONFIG.SEC_SERVER, CONFIG.KEY_IP, ip)

    try:
        port = con.getConfig(CONFIG.SEC_SERVER, CONFIG.KEY_PORT)
    except:
        port = PC_Port
        Command.config.setConfig(CONFIG.SEC_SERVER, CONFIG.KEY_PORT, str(port))

    Command.config, Command.IP, Command.port = con, ip, port


    Command.updateCommand()

    run(app, ip, int(port))




if __name__ == '__main__':
    start()