# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
protocol file
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/2 17:01"
__all__ = ["__version__", "MessageType", "pack", "unpack"]
__version__ = "1.0.0"

import struct
from enum import Enum, unique



@unique
class MessageType(Enum):
    EOF = b" -*-END-*-"
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    # invalid action
    invalid = -1

    # normal protocol
    # client to server
    connect = 1
    apps = 12

    update_app = 21

    disconnect = 41

    # server to client
    welcome = 101

    install = 121
    restart = 122
    update2client = 123

    uninstall = 141


def pack(MessageType, *args):
    fmt = ""
    for i in args:
        if isinstance(i, unicode):
            raise TypeError("-> %s <- is unicode type, Please convert it.")
        elif isinstance(i, int):
            fmt += "L"
        elif isinstance(i, float):
            fmt += "f"
        elif isinstance(i, bytes):
            fmt += str(len(i)) + "s"
        else:
            pass
    serializeMessage = struct.pack(fmt, *args)
    fmt_send = "!LLL" + str(len(fmt)) + "s" + str(len(serializeMessage)) + "s"
    serializeData = struct.pack(fmt_send, MessageType, len(fmt),
                                len(serializeMessage), fmt, serializeMessage)
    pack_to_send = serializeData
    return pack_to_send


def unpack(data):
    serializeMessage = data
    fmt = "!LLL"
    _t = struct.unpack_from(fmt, serializeMessage)
    get_message = [_t[0]]
    fmt += str(_t[1]) + "s" + str(_t[2]) + "s"
    _msg = struct.unpack(fmt, serializeMessage)
    res = struct.unpack(_msg[3].decode("utf8"), _msg[4])
    for i in res:
        get_message.append(i)
    return get_message