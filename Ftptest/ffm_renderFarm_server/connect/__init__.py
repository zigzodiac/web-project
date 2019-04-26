# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/2 16:54"
__all__ = ["__version__", "clients", "packMessage", "unpackMessage"]
__version__ = "1.0.0"
import json
from connect import protocol


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

    def get_s_all(self):
        return self.socket_register.values()

    def get_s_except_one(self, name):
        if not isinstance(name, str):
            try:
                name = str(name)
            except Exception:
                raise TypeError("name excepted one str or unicode argument.")

        res = self.get_s_all()
        try:
            res.remove(self.get_s(name))
        except:
            pass
        return res

    def add_s(self, name, s):
        if not any([name, s]):
            return False

        self._socket_register.update({name: s})

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

    def check_s_exist(self, s):
        return s in self.socket_register.values()

    def check_name_exist(self, name):
        return name in self.socket_register.keys()

    def _get_name_by_s(self, s):
        try:
            return [k for k, v in self.socket_register.items() if v == s][0]
        except:
            return None

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