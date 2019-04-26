# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/1/2 16:25"
__all__ = ["__version__", "STATE", "DB_CONFIGURE"]
__version__ = "1.0.0"
from enum import Enum, unique


DB_CONFIGURE = None  # database configure singleton instance.


@unique
class STATE(Enum):
    Start = 1
    Queue = 2
    Finish = 3
    Error = 4
    Other = 5

