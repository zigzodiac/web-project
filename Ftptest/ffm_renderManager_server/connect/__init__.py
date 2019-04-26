# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/1/2 16:54"
__all__ = ["__version__", "clients", "packMessage", "unpackMessage"]
__version__ = "1.0.0"
import json
from connect import protocol

import util


class _keep_conncet_manage(object):
    '''
    Manage all client connect socket.
    '''
    _socket_register = {}

    def __init__(self):
        pass

    @property
    def socket_register(self):
        return self._socket_register

    def get_rc(self, name):
        # print "get_rc", self.socket_register
        rc_key = name + '_rc'
        if not isinstance(rc_key, str):
            try:
                rc_key = str(rc_key)
            except Exception:
                raise TypeError("name excepted one str or unicode argument.")

        if rc_key in self.socket_register.keys():
            return self.socket_register[rc_key]
        else:
            return None

    def get_s(self, name):
        if not isinstance(name, str):
            try:
                name = str(name)
            except Exception:
                raise TypeError("name excepted one str or unicode argument.")

        if name in self.socket_register.keys():
            return self.socket_register[name]
        else:
            return None

    def get_name(self, s):
        return self._get_name_by_s(s)

    def get_rc_all(self):
        res = []
        for key, value in self.socket_register.items():
            if key.endswith("_rc"):
                res.append(value)
        return res

    def get_render_client(self, s):
        name = self._get_name_by_s(s)
        rc_key = name + '_rc'
        if rc_key in self.socket_register.keys():
            return self.socket_register[rc_key]
        else:
            return None

    def add_s(self, name, s, rc):
        if not any([name, s]):
            return False

        rc_key = name + '_rc'
        # self._socket_register.update({name: s})
        self._socket_register.update({name: s, rc_key: rc})

    def add_dict(self, d):
        if not isinstance(d, dict):
            return False

        self._socket_register.update(d)

    # def del_s(self, s):
    #     if not self.check_s_exist(s):
    #         return
    #
    #     name = self._get_name_by_s(s)
    #     del self.socket_register[name]

    def remove_s(self, s, name=None):
        if isinstance(s, str):
            name = s
        else:
            if not self.check_s_exist(s):
                return
            name = self._get_name_by_s(s)

        if name in self.socket_register.keys():
            del self.socket_register[name]

        rc_key = name + '_rc'
        if rc_key in self.socket_register.keys():
            self.socket_register[rc_key].destroy()
            del self.socket_register[rc_key]

    def check_s_exist(self, s):
        return s in self.socket_register.values()

    def check_name_exist(self, name):
        return name in self.socket_register.keys()

    def _get_name_by_s(self, s):
        try:
            return [k for k, v in self.socket_register.items() if v == s][0]
        except:
            return None

    def __check_name(self, name):
        if not name.endswith('_rc'):
            return True
        return False

    def __getitem__(self, item):
        return self.socket_register[item]

    def __len__(self):
        return len(self.socket_register)

    def __str__(self):
        return "%s" % self.socket_register

    def __repr__(self):
        return "%s" % self.socket_register


clients = _keep_conncet_manage()


def packMessage(type, message):
    s = protocol.pack(type, json.dumps(message))
    return s


def unpackMessage(message):
    type, new = protocol.unpack(message)
    return type, json.loads(new)


def sendMessageByName(username, TYPE, message):
    client = clients.get_s(username)
    if client:
        try:
            client.send_message(
                packMessage(TYPE.value, message)
            )
        except Exception as e:
            util.JLOG.error(e)
