# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/3/7 22:54"
__all__ = ["__version__", "start"]
__version__ = "1.1.0.0"
from widget.main_widget import run


def start():
    run()


if __name__ == '__main__':
    start()