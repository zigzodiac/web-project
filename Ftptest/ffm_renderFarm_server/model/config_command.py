# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/9 15:37"
__all__ = ["__version__", "Command"]
__version__ = "1.0.0"
from config import CONFIG



class _Command(object):
    def __init__(self):
        self.__config_file = None
        self.__config_instance = None
        self._install = dict()
        self._uninstall = dict()
        self._path = dict()
        self._ip = None
        self._port = None

    def addInstall(self, key, value):
        self._install.update({key: value})

    def addUninstall(self, key, value):
        self._uninstall.update({key: value})

    def addPath(self, key, value):
        self._path.update({key: value})

    def updateCommand(self):
        self.install.clear()
        self.uninstall.clear()
        self.path.clear()
        for key in self.config.getAllKeys(CONFIG.SEC_INSTALL):
            self.addInstall(
                key, self.config.getConfig(CONFIG.SEC_INSTALL, key)
            )

        for key in self.config.getAllKeys(CONFIG.SEC_UNINSTALL):
            self.addUninstall(
                key, self.config.getConfig(CONFIG.SEC_UNINSTALL, key)
            )

        for key in self.config.getAllKeys(CONFIG.SEC_PATH):
            self.addPath(
                key, self.config.getConfig(CONFIG.SEC_PATH, key)
            )

    def removeCommand(self):
        for k in self.config.getAllKeys(CONFIG.SEC_INSTALL):
            self.config.delKey(CONFIG.SEC_INSTALL, k)

        for k in self.config.getAllKeys(CONFIG.SEC_UNINSTALL):
            self.config.delKey(CONFIG.SEC_UNINSTALL, k)

        for k in self.config.getAllKeys(CONFIG.SEC_PATH):
            self.config.delKey(CONFIG.SEC_PATH, k)

    def setCommand(self, key, path, install_v, uninstall_v):
        self.config.setConfig(CONFIG.SEC_INSTALL, key, install_v)
        self.config.setConfig(CONFIG.SEC_UNINSTALL, key, uninstall_v)
        self.config.setConfig(CONFIG.SEC_PATH, key, path)

    @property
    def install(self):
        return self._install

    @property
    def uninstall(self):
        return self._uninstall

    @property
    def path(self):
        return self._path

    @property
    def config(self):
        return self.__config_instance

    @config.setter
    def config(self, c):
        self.__config_instance = c

    @property
    def configFile(self):
        return self.__config_file

    @configFile.setter
    def configFile(self, f):
        self.__config_file = f

    @property
    def IP(self):
        return self._ip

    @IP.setter
    def IP(self, ip):
        self._ip = ip

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, p):
        self._port = p

    @property
    def restartCommand(self):
        return "shutdown /r"





Command = _Command()
