# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/2 17:01"
__all__ = ["__version__", "ConnectThread"]
__version__ = "1.0.0"
import threading
import json
from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop
from tornado import gen
from tornado import iostream

from config import PARAM
from connect import protocol
from connect import unpackMessage
import connect
from model.client_model import RenderClient
import widget
import util



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
        try:
            name = connect.clients.get_name(self)
            ip = self._address[0]
            if name:
                util.JLOG.printInfo("Disconnect: " + str(name), self)
                widget.JWindow.DISCONNECT_SIGNAL.emit({PARAM.NAME: name, PARAM.IP: ip})
            connect.clients.remove_s(self)
        except Exception as e:
            util.JLOG.warning("On close has a error: %s" % e)
        finally:
            try:
                self._stream.close()
            except:
                pass

    def _add_client(self, name):
        render_client = RenderClient(name)
        connect.clients.add_s(name, self, render_client)

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
            if _msg.startswith("C#UPDATEINFO:"):
                type = protocol.MessageType.CS_UPDATE.value
                message = json.loads(_msg.split("C#UPDATEINFO:")[1])
            else:
                type, message = unpackMessage(_msg)
        except Exception as e:
            util.JLOG.error("unknown message can not unpack: %s" % _msg)
            return

        util.JLOG.printInfo("received: " + str(type), message)

        if type == protocol.MessageType.connect.value:
            # New client connect, check password, create client model.
            if connect.clients.get_s(message[PARAM.NAME]):
                connect.clients.get_s(message[PARAM.NAME]).on_close()

            self._add_client(message[PARAM.NAME])
            message.update({PARAM.IP: self._address[0]})
            widget.JWindow.CONNECT_SIGNAL.emit(message)

        elif type == protocol.MessageType.disconnect.value:
            self.on_close()

        elif type == protocol.MessageType.get_app_versions.value:
            widget.JWindow.GET_SOFT_VERSION_SIGNAL.emit(message)

        elif type == protocol.MessageType.get_ftp_info.value:
            widget.JWindow.GET_FTP_SIGNAL.emit(message)

        elif type == protocol.MessageType.get_error_messages.value:
            # Get error details.
            widget.JWindow.GET_ERROR_SIGNAL.emit(message)

        elif type == protocol.MessageType.get_file_valid.value:
            # Check file valid on server disk
            widget.JWindow.GET_FILE_VALID_SIGNAL.emit(message)

        # ============ about job type ============
        elif type == protocol.MessageType.render_submit.value:
            # print "Submit Job!"
            widget.JWindow.SUBMIT_SIGNAL.emit(message)

        elif type == protocol.MessageType.render_cancel.value:
            # print "Job cancel"
            widget.JWindow.CANCEL_SIGNAL.emit(message)

        elif type == protocol.MessageType.render_update.value:
            # print "Job update!"
            widget.JWindow.JOB_UPDATE_SIGNAL.emit(message)

        elif type == protocol.MessageType.pay_request.value:
            widget.JWindow.PAY_R_SIGNAL.emit(message)

        elif type == protocol.MessageType.CS_UPDATE.value:
            # print "C# update information:", message
            widget.JWindow.CS_UPDATE_SIGNAL.emit(message)


        # ======= Deadline to server =======
        # elif type == protocol.MessageType.DLR_Start.value:
        #     client_name = message['UserName']
        #     render_client = connect.clients.get_rc(client_name)
        #     render_client.clientJobStart(message)
        #     # widget.JWindow.START_TASK_SIGNAL.emit(message)
        #
        # elif type == protocol.MessageType.DLR_Finish.value:
        #     client_name = message['UserName']
        #     render_client = connect.clients.get_rc(client_name)
        #     render_client.clientJobFinish(message)
        #     widget.JWindow.FINISH_SIGNAL.emit(message)
        #
        # elif type == protocol.MessageType.DLR_Error.value:
        #     client_name = message['UserName']
        #     render_client = connect.clients.get_rc(client_name)
        #     render_client.render_job_error(message)
        #     widget.JWindow.CANCEL_SIGNAL.emit(message)


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
        server.listen(int(self.port), self.ip)
        self.io.start()

    def stop(self):
        self.io.stop()

