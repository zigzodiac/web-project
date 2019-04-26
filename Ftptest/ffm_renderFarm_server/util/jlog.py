# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
工作中使用的简单log封装。
通过JLog(文件名，等级，日志实例名称) 创建一个log实例对象，参数全部有默认。
 # 文件可以后续添加，默认初始化无文件状态，但是输出日志时只会打印在终端；
     # 使用log.file = "文件名" 添加文件
 # 等级默认为DEBUG
     # 日志对象拥有8个等级，分别是
     # "NOTSET", "DEBUG", "INFO", "WARNING", "WARN", "ERROR", "FATAL", "CRITICAL"
     # 使用log.setLevel(lv) 或者 log.level = lv 来设置日志输出等级
     # 使用log.getLevel() 或者 log.level 来查看当前等级
 # 实例名称用于给当前实例命名
     # 默认为"logger"，如果创建实例时没有给出名称，使用默认名称，并没有提供修改函数。
     # 使用log.name 来查看当前命名

创建好log对象后，直接使用对应函数输出日志信息
log.debug(), log.info(), log.warning(),
log.error(), log.fatal(), log.critical()

一个简单的函数日志装饰器，直接使用@j_log添加装饰器即可，可以打印错误日志。
一个简单的类装饰器，使用@JLogDecorator添加，除打印错误日志外，开可以添加额
外其他方法，方便使用。

v 1.0.1 update information:
- add a decorator class
- modify a decorator function
    it can add log file
- modify JLog class
    add set file function (self.file = 'filename')
    add get file function (self.file)
    add get name function (self.name)
    add a function force the print message to the terminal (self.printInfo())
"""
from __future__ import unicode_literals
__author__ = "jeremyjone"
__datetime__ = "2018/12/29 18:10"
__all__ = ["__version__", "JLog", "j_log", "JLogDecorator", "LOG_LEVEL_KEY"]
__update_time__ = "2019/01/14 12:10"
__version__ = "1.0.1"

import logging
import sys
import os
from functools import wraps


LOG_LEVEL_KEY = ["", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class JLog(object):
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"
    CRITICAL = "CRITICAL"

    __level = {
        "NOTSET": logging.NOTSET,
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "WARN": logging.WARN,
        "ERROR": logging.ERROR,
        "FATAL": logging.FATAL,
        "CRITICAL": logging.CRITICAL,
    }

    def __init__(self, log_file=None, level="DEBUG", name="logger"):
        self.__showLevel = self.__level[level]
        if log_file and not os.path.exists(os.path.dirname(log_file)):
            os.makedirs(os.path.dirname(log_file))
        self.__log_file = log_file
        # 创建日志的实例
        self.__logger = logging.getLogger(name)
        self.__setLog()

    def __setLog(self):
        # 指定Logger的输出格式
        self.formatter = logging.Formatter("%(asctime)s  %(levelname)s \n\t%(message)s")
        # 设置默认的日志级别
        self.__logger.setLevel(self.__showLevel)
        if self.__log_file:
            self.__createLog(self.__log_file)

    def __createLog(self, file):
        # 创建文件日志
        self.__file_handler = logging.FileHandler(file)
        self.__file_handler.setFormatter(self.formatter)
        # 创建终端日志
        self.__console_handler = logging.StreamHandler(sys.stdout)
        self.__console_handler.setFormatter(self.formatter)
        # 把文件日志和终端日志添加到日志处理器中
        self.__logger.addHandler(self.__file_handler)
        self.__logger.addHandler(self.__console_handler)

    def close(self):
        # 当不再使用这个日志Handle时。需要remove
        self.__logger.removeHandler(self.__file_handler)
        self.__logger.removeHandler(self.__console_handler)

    def setLevel(self, level):
        if level not in self.__level:
            raise TypeError("set valid log level.")

        self.__logger.setLevel(self.__level[level])
        self.__showLevel = self.__level[level]

    def getLevel(self):
        return [k for k, v in self.__level.items() if v == self.__showLevel][0]

    @property
    def name(self):
        return self.logger.name

    @property
    def level(self):
        return self.getLevel()

    @level.setter
    def level(self, lv):
        self.setLevel(lv)

    @property
    def file(self):
        return self.__log_file

    @file.setter
    def file(self, f):
        # self.close()
        if f and not os.path.exists(os.path.dirname(f)):
            os.makedirs(os.path.dirname(f))
        self.__log_file = f
        self.__createLog(f)

    @property
    def logger(self):
        return self.__logger

    def printInfo(self, *args):
        r = ""
        for a in args:
            if r:
                r += ", "
            r += a.__str__()

        _l = self.level
        self.level = self.INFO
        self.info(r)
        self.level = _l

    def debug(self,  msg, *args, **kwargs):
        self.__logger.debug( msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.__logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.__logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.__logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.__logger.critical(msg, *args, **kwargs)

    fatal = critical





def j_log(log):
    '''
    Use this decorator when an operation fails and no additional operations are required.

    :param func: The function that is decorated.
    :return: decorated function.
    '''
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log.error("function name: %s, message is: %s"
                          % (func.__name__, str(e))
                          )
        return wrapped_function
    return logging_decorator


class JLogDecorator(object):
    def __init__(self, log):
        self.log = log

    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            # 执行添加的功能
            self.notify()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # 打印日志
                self.log.error("function name: %s, message is: %s"
                               % (func.__name__, str(e))
                               )
        return wrapped_function

    def notify(self):
        # 添加一个功能
        print("notify")







if __name__ == '__main__':
    log1 = JLog("d:/t/log")

    # print(log1.getLevel())
    # log1.setLevel(log1.ERROR)
    # print(log1.getLevel())

    # print(log1.level)
    # log1.level = log1.FATAL
    # print(log1.level)
    # log1.level = log1.DEBUG
    # print(log1.getLevel())

    # log1.warning("这是一条warning信息")
    # log1.logger.error("这是error错误")

    @j_log(log1)
    def test():
        a = "1,test a"
        print(a)
        if not isinstance(a, int):
            raise TypeError("Type error")


    # test()

    # print(log.file)
    # log.file = "d:\\test\\log"
    # print(log.file)

    # print(log.level)
    test()

    log1.close()

    log2 = JLog(name="123")

    @JLogDecorator(log2)
    def test2():
        b = "2,test b"
        print(b)
        if not isinstance(b, int):
            raise TypeError("Type error111")


    test2()
    print(log2.name)

    # JLOG.file = "d:\\test\\log1"
    #
    # print(JLOG.level)
    # print(JLOG.file)
    # JLOG.info("aaaaaaaaaaaaaaaaaaaa")
    #
    # JLOG.level = JLOG.ERROR
    #
    # JLOG.warning("wwwwwwwwwwwwwwwww")
    #
    # JLOG.printInfo("ppppppppppppppppppp")
    #
    # JLOG.warning("vvvvvvvvvvvvvvvvvvvvvvvv")
    # JLOG.error("eeeeeeeeeeeeeeee")
