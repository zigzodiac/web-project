# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/3 10:28"
__all__ = ["__version__", ]
__version__ = "1.0.0"


def openPath(filename):
    import os
    import subprocess
    file = filename.encode("utf8")
    try:
        os.startfile(file)
    except:
        subprocess.Popen(['xdg-open', file])


def convertFileSizeFormat(size):
    g = size / 1024.0 / 1024.0 / 1024.0
    if g < 1.0:
        m = g * 1024.0
        if m < 1.0:
            k = m * 1024.0
            return "{0:.2f} KB".format(k)
        else:
            return "{0:.2f} MB".format(m)
    else:
        return "{0:.2f} GB".format(g)


def getLocalDrives():
    import _winreg
    res = []
    subKey = 'SYSTEM\MountedDevices'
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, subKey)
    i = 0
    try:
        while True:
            name, value, type = _winreg.EnumValue(key, i)
            if name.startswith('\\DosDevices\\'):
                sp = name.split('\\')
                res.append(sp[-1])
            i += 1
    except WindowsError:
        pass
    return res