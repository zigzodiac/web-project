# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/3 10:32"
__all__ = ["__version__", ]
__version__ = "1.0.0"

import threading
from tornado import ioloop, gen, iostream
from tornado.tcpclient import TCPClient

import connect
from connect import protocol
from connect import packMessage, unpackMessage
from path.versions import Viersions
import widget
from config.logger import Logger

import socket


def test_request():
    user_name = socket.gethostname()
    user_addr = socket.gethostbyname(user_name)
    apps = Viersions().getVersions()

    msg = packMessage(protocol.MessageType.connect.value, {"PC-Name": user_name, "APPS": apps.keys()})
    return msg


class _ChatClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.EOF = protocol.MessageType.EOF.value

    @gen.coroutine
    def start(self, timeout=0):
        try:
            Logger.info("start...")
            self.stream = yield TCPClient().connect(self.host, self.port)
            widget.JWindow.setStatus('Connect')
            connect.Client = self
            message = test_request()
            yield self.stream.write(message + self.EOF)
            yield self.receive_message()
            yield self.send_message()
        except iostream.StreamClosedError as e:
            widget.JWindow.setStatus('Disconnect')
            connect.Client = None
            Logger.error(e)

        except Exception as e:
            widget.JWindow.setStatus('Disconnect')
            connect.Client = None
            self.stream.close()
            Logger.error(e)

    @gen.coroutine
    def send_message(self, data=str(protocol.MessageType.invalid.value)):
        try:
            yield self.stream.write(data + self.EOF)

        except Exception as e:
            Logger.error(e)
            self.stream.close()

    @gen.coroutine
    def receive_message(self):
        while True:
            try:
                data = yield self.stream.read_until(self.EOF)
                self._handle_message(data)
            except iostream.StreamClosedError:
                widget.JWindow.setStatus('Disconnect')
                connect.Client = None
                break
            except Exception as e:
                Logger.error(e)
                self.stream.close()
                break

    def _handle_message(self, data):
        _msg = data.split(self.EOF)[0]
        type, message = unpackMessage(_msg)
        print "received", type, message

        if type == protocol.MessageType.welcome.value:
            print message

        elif type == protocol.MessageType.uninstall.value:
            print "uninstall", message
            widget.JClientReceive.UNINSTALL_SIGNAL.emit(message)

        elif type == protocol.MessageType.install.value:
            print "install", message
            widget.JClientReceive.INSTALL_SIGNAL.emit(message)

        elif type == protocol.MessageType.restart.value:
            print "restart", message
            widget.JClientReceive.RESTART_SIGNAL.emit(message)

        elif type == protocol.MessageType.update2client.value:
            print "reconnect", message
            widget.JClientReceive.RESEND_SIGNAL.emit()


def client_connect(address):
    if not isinstance(address, tuple):
        raise TypeError("address must be tuple include IP and port.")

    c = _ChatClient(*address)
    c.start()

    return c


class ConnectThread(threading.Thread):
    name = "connect server thread"

    def __init__(self, address):
        self.address = address
        super(ConnectThread, self).__init__()
        self.io = None
        self.chat_client = None

    def run(self):
        self.io = ioloop.IOLoop.instance()
        self.chat_client = client_connect(self.address)
        self.io.start()

    def stop(self):
        if self.io.stop():
            self.io.stop()
            self.io = None

        if hasattr(self.chat_client, 'stream'):
            self.chat_client.stream.close()
            self.chat_client = None
