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
import widget
import pprint


class _ChatClient(object):
    def __init__(self, host, port, id, pw):
        self.host = host
        self.port = port

        self.user_id = id
        self.user_pw = pw
        
        self.EOF = protocol.MessageType.EOF.value

    @gen.coroutine
    def start(self, timeout=0):
        try:
            print("start...")
            widget.JWindow.STATUS_MESSAGE_SIGNAL.emit('Please wait a second. '
                                                      'Now try to login service.')

            self.stream = yield TCPClient().connect(self.host, self.port)
            connect.Client = self
            message = packMessage(protocol.MessageType.connect.value, {"UserName": self.user_id, "PassWord": self.user_pw})
            yield self.stream.write(message + self.EOF)
            yield self.receive_message()
            yield self.send_message()
            
        except iostream.StreamClosedError as e:
            widget.JWindow.DISCONNECT_SIGNAL.emit(e)
            widget.JWindow.STATUS_MESSAGE_SIGNAL.emit('Server not response. '
                                                      'If you can\'t login again contact with Administrator.')

        except Exception as e:
            widget.JWindow.DISCONNECT_SIGNAL.emit(e)
            widget.JWindow.STATUS_MESSAGE_SIGNAL.emit('Server not response. '
                                                      'If you can\'t login again contact with Administrator.')

    @gen.coroutine
    def send_message(self, data=str(protocol.MessageType.invalid.value)):
        try:
            yield self.stream.write(data + self.EOF)

        except Exception as e:
            widget.JWindow.STATUS_MESSAGE_SIGNAL.emit('Something wrong. '
                                                      'Please make sure correct command.')
            self.stream.close()

    @gen.coroutine
    def receive_message(self):
        while True:
            try:
                data = yield self.stream.read_until(self.EOF)
                self._handle_message(data)
            except iostream.StreamClosedError:
                widget.JWindow.STATUS_MESSAGE_SIGNAL.emit('Something wrong. '
                                                          'Please make sure correct command.')
                widget.JWindow.DISCONNECT_SIGNAL.emit(dict())
                break
            except Exception as e:
                widget.JWindow.STATUS_MESSAGE_SIGNAL.emit('Something wrong. '
                                                          'Please make sure correct command.')
                widget.JWindow.DISCONNECT_SIGNAL.emit(e)
                break

    def _handle_message(self, data):
        _msg = data.split(self.EOF)[0]
        type, message = unpackMessage(_msg)
        # print "received", type, message
        # print "received", type
        # pprint.pprint(message)

        if type == protocol.MessageType.welcome.value:
            # print ('Connected : %s' % message)
            widget.JWindow.CONNECT_SIGNAL.emit(message)

        elif type == protocol.MessageType.get_ftp_info_from_server.value:
            print ' : Set Ftp Info'
            widget.JWindow.GET_FTP_INFO_SIGNAL.emit(message)

        elif type == protocol.MessageType.change_pay_state.value:
            print ('Change Pay State : %s' % message)
            widget.JWindow.CHANGE_JOB_PAYMENT_SIGNAL.emit(message)

        elif type == protocol.MessageType.user_info.value:
            print ('User Info')
            # pprint.pprint(message)
            widget.JWindow.INIT_SIGNAL.emit(message)

        elif type == protocol.MessageType.job_list.value:
            print ('Job Update')
            # pprint.pprint(message)
            widget.JWindow.UPDATE_JOB_LIST_SIGNAL.emit(message)

        elif type == protocol.MessageType.disconnect.value:
            print message
            widget.JWindow.DISCONNECT_SIGNAL.emit(message)

        elif type == protocol.MessageType.declined.value:
            print message
            widget.JWindow.DISCONNECT_SIGNAL.emit(message)

        elif type == protocol.MessageType.render_submit.value:
            print ' : Render_submit'
            widget.JWindow.RENDER_SUBMIT_SIGNAL.emit(message)

        elif type == protocol.MessageType.render_start.value:
            print ' : Render_start'
            widget.JWindow.RENDER_START_SIGNAL.emit(message)

        elif type == protocol.MessageType.render_finish.value:
            print ' : Render_finish'
            pprint.pprint(message)
            widget.JWindow.RENDER_FINISH_SIGNAL.emit(message)

        elif type == protocol.MessageType.render_error.value:
            print ' : Render_error'
            pprint.pprint(message)
            widget.JWindow.RENDER_ERROR_SIGNAL.emit(message)

        elif type == protocol.MessageType.send_error_count_from_server.value:
            print ' : Render_error'
            pprint.pprint(message)
            widget.JWindow.RENDER_ERROR_SIGNAL.emit(message)

        elif type == protocol.MessageType.render_cancel.value:
            print ' : Render_cancel'
            pprint.pprint(message)
            widget.JWindow.RENDER_CANCEL_SIGNAL.emit(message)

        elif type == protocol.MessageType.render_progress.value:
            # print ' : Rendering Job State', message
            widget.JWindow.RENDERPROGRESS_JOB_ITEM_SIGNAL.emit(message)

        elif type == protocol.MessageType.get_app_versions_from_server.value:
            # print ' : Set App Versions : ', message
            widget.JWindow.submit_dialog.GET_VERSIONS_SIGNAL.emit(message)

        elif type == protocol.MessageType.get_error_messages_from_server.value:
            print ' : Get Error Message '
            widget.JWindow.SHOW_ERRORS_SIGNAL.emit(message)

        elif type == protocol.MessageType.submit_result_from_server.value:
            print ' : Get Submit Result Message '
            widget.JWindow.SUBMIT_RESULT_SIGNAL.emit(message)

        elif type == protocol.MessageType.get_file_valid_from_server.value:
            print ' : Get File Valid From Server '
            widget.JWindow.submit_dialog.GET_FILE_VALID_SIGNAL.emit(message)


def client_connect(args):
    if not isinstance(args, tuple):
        raise TypeError("address must be tuple include IP and port.")

    c = _ChatClient(*args)
    c.start()

    return c


class ConnectThread(threading.Thread):
    name = "connect server thread"

    def __init__(self, args):
        self.args = args
        super(ConnectThread, self).__init__()
        self.io = None
        self.chat_client = None

    def run(self):
        self.io = ioloop.IOLoop.instance()
        self.chat_client = client_connect(self.args)
        self.io.start()

    def stop(self):
        if self.io.stop():
            self.io.stop()
            self.io = None

        if hasattr(self.chat_client, 'stream'):
            self.chat_client.stream.close()
            self.chat_client = None
