# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/3 10:28"
__all__ = ["__version__", "packMessage", "unpackMessage"]
__version__ = "1.0.0"
import json
from connect import protocol

Client = None


def packMessage(type, message):
    s = protocol.pack(type, json.dumps(message))
    return s



def unpackMessage(message):
    type, new = protocol.unpack(message)
    return type, json.loads(new)

