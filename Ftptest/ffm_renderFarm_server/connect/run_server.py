# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/2 17:01"
__all__ = ["__version__", ]
__version__ = "1.0.0"
import threading
from functools import wraps
from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop
from tornado import gen
from tornado import iostream

from connect import protocol
from connect import unpackMessage
import connect
import util
import widget
from config import PARAM




class Connection(object):
    def __init__(self, stream, address):
        self.EOF = protocol.MessageType.EOF.value

        self._stream = stream
        self._address = address
        self._stream.set_close_callback(self.on_close)

    @gen.coroutine
    def send_message(self, data):
        try:
            yield self._stream.write(data + self.EOF)
        except Exception as e:
            util.JLOG.error(e)

    def on_close(self):
        name = connect.clients.get_name(self)
        util.JLOG.printInfo("Disconnect: " + str(name), self)
        ip = self._address[0]
        if name:
            widget.JWindow.DISCONNECT_SIGNAL.emit({PARAM.NAME: name, PARAM.IP: ip})
        connect.clients.remove_s(self)
        self._stream.close()

    def _add_client(self, name):
        connect.clients.add_s(name, self)

    @gen.coroutine
    def read_message(self):
        while True:
            try:
                _m = yield self._stream.read_until(self.EOF)
                self._handle_message(_m)
            except iostream.StreamClosedError:
                break
            except Exception as e:
                util.JLOG.error(e)
                self._stream.close()
                self.on_close()
                break

    def _handle_message(self, data):
        '''
        Message checking, distribution.
        All received message needs to go through here.

        Unpack failed, log back directly, If you connect to an unregistered
        socket, send login failure message to client, reject the operation.

        :param data: struct type, data package.
        '''

        try:
            _msg = data.split(self.EOF)[0]
        except Exception as e:
            util.JLOG.warning("handle message format error...")
            self.on_close()
            return

        if _msg == str(protocol.MessageType.invalid.value):
            return

        try:
            type, message = unpackMessage(_msg)
        except Exception as e:
            util.JLOG.warning("unknown message can not unpack: %s" % _msg)
            return

        util.JLOG.printInfo("received: " + str(type), message)
        if type == protocol.MessageType.connect.value:
            if connect.clients.get_s(message[PARAM.NAME]):
                connect.clients.get_s(message[PARAM.NAME]).on_close()

            self._add_client(message[PARAM.NAME])
            message.update({PARAM.IP: self._address[0]})
            widget.JWindow.CONNECT_SIGNAL.emit(message)

        elif type == protocol.MessageType.disconnect.value:
            widget.JWindow.DISCONNECT_SIGNAL.emit(message)

        elif type == protocol.MessageType.update_app.value:
            name = connect.clients.get_name(self)
            m = {PARAM.NAME: name, PARAM.APPS: message}
            widget.JWindow.UPDATE_APP_SIGNAL.emit(m)


class JServer(TCPServer):
    '''
    Inherit TCPServer, duplicate handle_stream.
    Messages can be sent and received through stream(IOStream type).
    '''
    @gen.coroutine
    def handle_stream(self, stream, address):
        conn = Connection(stream, address)
        yield conn.read_message()



class ConnectThread(threading.Thread):
    name = "connect server thread"
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        super(ConnectThread, self).__init__()

    def run(self):
        self.io = IOLoop.instance()
        server = JServer()
        server.listen(self.port, self.ip)
        self.io.start()

    def stop(self):
        self.io.stop()

