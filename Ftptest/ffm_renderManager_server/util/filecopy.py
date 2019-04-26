#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ctypes, sys, os

# .so file is located in the directory above. See Makefile for
# build instructions
if "win" in sys.platform:
    _path = r'./util/libfilecopy2-win.dll'
else:
    _path = r'./util/libfilecopy2-linux.so'
_mod = ctypes.cdll.LoadLibrary(_path)


_file_copy = _mod.file_copy
_file_copy.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p)
_file_copy.restype = ctypes.c_int

def copyFile(srcPath, dstPath):
    return _file_copy(srcPath, dstPath)

_getcopysize = _mod.getcopysize
_getcopysize.argtypes = ()
_getcopysize.restype = ctypes.c_int64


def getcopysize():
    return _getcopysize()


_setcopysize = _mod.setcopysize
_setcopysize.argtypes = ()
_setcopysize.restype = ctypes.c_int


def setcopysize():
    return _setcopysize()



