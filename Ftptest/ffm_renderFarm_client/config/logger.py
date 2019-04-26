#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
author:bl
time:2018/12/13 17:54

"""
import os
import sys
import logging
import socket

from ffm.config.jconfig import JConfig

user_name = socket.gethostname()
user_addr = socket.gethostbyname(user_name)
log_path = JConfig('./config.cfg').getConfig('Path', 'log_path')
LOG_FILE = os.path.join(log_path, user_addr + '-' + user_name + '.cfg')

class _Logger(object):
    logger = logging.getLogger("logger")
    logger_file = LOG_FILE

    def __init__(self):
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

        file_handler = logging.FileHandler(self.logger_file)
        file_handler.setFormatter(formatter)

        control_handler = logging.StreamHandler(sys.stderr)
        control_handler.setFormatter(formatter)

        self.logger.setLevel(logging.INFO)

        self.logger.addHandler(file_handler)

        self.logger.addHandler(control_handler)


Logger = _Logger().logger


if __name__ == '__main__':

    Logger.info('it ok')
    Logger.warning('it ok1')
    Logger.warning('it ok2')




