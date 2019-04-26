# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/3 16:48"
__all__ = ["__version__", ]
__version__ = "1.0.0"



class JSelectItem(object):
    def __init__(self):
        self.__data = dict()

    def __repr__(self):
        return self.__data.__repr__()

    def __str__(self):
        return self.__data.__str__()

    def update(self, k, v):
        if not self.__data.get(k):
            self.__data[k] = set()

        self.__data[k].add(v)

    def __getitem__(self, item):
        return self.__data[item]

    def __setitem__(self, key, value):
        self.update(key, value)

    def delete(self, key, value):
        if self.__data.get(key):
            try:
                self.__data[key].remove(value)
            except:
                pass

        if not self.__data.get(key):
            self.__delitem__(key)

    def keys(self):
        return self.__data.keys()

    def __delitem__(self, key):
        try:
            del self.__data[key]
        except:
            pass

    def __iter__(self):
        for key in self.__data:
            yield key, self.__data[key]
        else:
            raise StopIteration
