#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
author:bl
time:2019/1/3 12:09

"""
import os
import glob
import config

from ffm.config.jconfig import JConfig


class Viersions(object):
    def __init__(self):
        self.versions = dict()
        self.config_cfg = JConfig(config.CONFIG_FILE)

    def __get(self, path_key, app_path):
        bin_path = os.path.join(app_path, 'bin')
        if os.path.exists(bin_path):
            for fpathe, dirs, fs in os.walk(bin_path):
                for f in fs:
                    if os.path.splitext(f)[-1] == ".exe":
                        self.versions[path_key] = self.config_cfg.getConfig(config.CONFIG_PATH_SECTION, path_key)
                        return

        if len(glob.glob(os.path.join(app_path, "*.exe"))) > 0:
            self.versions[path_key] = self.config_cfg.getConfig(config.CONFIG_PATH_SECTION, path_key)

    def getVersions(self):
        self.versions.clear()

        path_keys = self.config_cfg.getAllKeys(config.CONFIG_PATH_SECTION)
        for path_key in path_keys:
            app_path = self.config_cfg.getConfig(config.CONFIG_PATH_SECTION, path_key)
            self.__get(path_key, app_path)

        return self.versions


if __name__ == '__main__':
    version = Viersions()
