# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/4 10:31"
__all__ = ["__version__", ]
__version__ = "1.0.0"
import os
import shutil

import util


# def maya(path):
#     """Setup.exe / W / Q / I YOURFILENAME.ini / Lang en-US """
#     # "/W /q /I Img\maya2018_3.ini /language en-us"
#     cmd = "%s /W /q /I /language en-us" % path
#     return cmd


def houdini(path):
    cmd = '%s /S /AcceptEula=yes /LicenseServer=No ' \
          '/DesktopIcon=Yes /FileAssociations=Yes /HoudiniServer=No ' \
          '/EngineUnity=No /EngineMaya=No /EngineUnreal=No /HQueueServer=No ' \
          '/HQueueClient=No /IndustryFileAssociations=Yes /ForceLicenseServer=No ' \
          '/MainApp=Yes /Registry=Yes' % path
    return cmd


# def mark(path):
#     cmd = "%s /install /silent=Yes /force=Yes" % path
#     return cmd


def autodesk(path):
    dir = os.path.dirname(path).replace("/", "\\")
    if dir.split("\\")[-1] == "Img":
        dir = os.sep.join(dir.split("\\")[:-1])

    p = os.path.join(dir, "Img", "Setup.exe")
    ini = os.path.join(dir, "Img", "autodesk.ini")

    cmd = "'%s' /W /q /I '%s' /language zh-CN" % (p, ini)
    return cmd


def getHostIP():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def copyFile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        raise EOFError("%s not exist!")
    else:
        fpath, fname = os.path.split(dstfile)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        if not os.path.exists(dstfile):
            with open(dstfile, "wb") as wf:
                wf.write("")
        try:
            shutil.copy2(srcfile, dstfile)
            util.JLOG.info("OK! copy %s -> %s complete" % (srcfile, dstfile))
        except:
            raise