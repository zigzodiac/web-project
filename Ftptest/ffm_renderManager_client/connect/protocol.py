# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
protocol file
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/2 17:01"
__all__ = ["__version__", "MessageType", "pack", "unpack"]
__version__ = "1.0.0"

import struct
from enum import Enum, unique



@unique
class MessageType(Enum):
    EOF = b" -*-END-*-"
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    # invalid action
    invalid = -1

    # normal protocol
    # client to server
    connect = 1
    disconnect = 41

    # server to client
    welcome = 101   # 'Welcome FFM Render Manager'

    '''
        get job data
        comment: i["Props"]["Cmmt"], 
        name: i["Props"]["Name"], 
        path: i["Props"]["PlugInfo"]["ProjectPath"], 
        starttime: i["DateStart"], 
        endtime: i["DateComp"], 
        cost: i.get("Cost"),     # custom properties, if None, not key
        payment: i.get("PayState"),    # custom properties, if None, not key
        errorNumber: i["Errs"], 
        taskNumber: i["Props"]["Tasks"], 
        completeNumber: i["CompletedChunks"],  progress = completeNumber / taskNumber
        '''
    job_list = 102  # All Job information
    user_info = 105
    get_ftp_info_from_server = 103
    get_app_versions_from_server = 104
    get_error_messages_from_server = 106  # {'Errors': [{'Date': '2019-01-29 04:37:25', 'Frames': u'1-1', 'JobName': u'sdfasf', 'Type': 2, 'Title': u'Task rendering stopped due to external cancellation'}], 'Result': 'Success'}
    send_error_count_from_server = 107  # {"job_id": id, "Errs": 5}

    """
        {'Result': 'Success'}
        {'Result': 'Failed', 'ErrorFile': ['file1_path', 'file2_path']}
    """
    submit_result_from_server = 108
    get_file_valid_from_server = 109

    """
        {'Result': 'Success', "_id": job_id, "PayState": bool, True or False, "TotalBalance": 1.11}
        {'Result': 'Failed', "_id": job_id, 'Reason': '...'}
    """
    change_pay_state = 111
    declined = 144   # 'Server rejects login'


    render_progress = 151    # {u'UserName': self.username, u'job_id': job_id, u'complete': u"100"}

    # client render request
    '''
        FileInfo : ['zip filename'
                    {'Local': 'filename',
                    'Ftp': 'filename'}]
    '''
    render_submit = 201
    render_start = 202
    render_finish = 203
    render_error = 204
    render_cancel = 205
    render_update = 206
    render_wait = 207

    # Get Data
    '''
        From Client : {u'UserName': self.username, u'AppName': "MAYA / MAX / HOUDINI / C4D / NUKE"}

        Server Response Message :
            {'Result': 'Success', 'Versions': ['2016', '2017', '2018']}
            {'Result': 'Failed'}
    '''
    get_app_versions = 301

    '''
        From Client : {u'UserName': self.username}
        Server Response Message :
            {'Result': 'Success', 'FtpPath': r"\\192.168.1.47\share\Data\FTP", "FtpId": 'test1', "FtpPw": 'FFM@ftp!'} 
             // Real Network Share Path. Not Ftp Protocol Path (ftp://192.168.1.47)

            {'Result': 'Failed'}
    '''
    get_ftp_info = 302

    '''
        From Client : {u'UserName': self.username, 'job_id': '0000000'}
        Server Response Message :
            {'Result': 'Success', 'Errors': ['error1', 'error2', 'error3']} 
            {'Result': 'Failed'}
    '''
    get_error_messages = 303

    '''
        From Client : {u'UserName': self.username, 
                       u'FileInfo': [{"Local": path, "Ftp": path}, {...}]
                       }
        Server Response Message :
            {'Result': 'Success'} 
            {'Result': 'Failed', 'Errors': [path1, path2, ...]}
    '''
    get_file_valid = 304

    pay_request = 305  # {u'UserName': name, u'job_id': ...}

    # deadline to server
    DLR_Start = 2002
    DLR_Finish = 2003
    DLR_Error = 2004

def pack(MessageType, *args):
    fmt = ""
    for i in args:
        if isinstance(i, unicode):
            raise TypeError("-> %s <- is unicode type, Please convert it.")
        elif isinstance(i, int):
            fmt += "L"
        elif isinstance(i, float):
            fmt += "f"
        elif isinstance(i, bytes):
            fmt += str(len(i)) + "s"
        else:
            pass
    serializeMessage = struct.pack(fmt, *args)
    fmt_send = "!LLL" + str(len(fmt)) + "s" + str(len(serializeMessage)) + "s"
    serializeData = struct.pack(fmt_send, MessageType, len(fmt),
                                len(serializeMessage), fmt, serializeMessage)
    pack_to_send = serializeData
    return pack_to_send


def unpack(data):
    serializeMessage = data
    fmt = "!LLL"
    _t = struct.unpack_from(fmt, serializeMessage)
    get_message = [_t[0]]
    fmt += str(_t[1]) + "s" + str(_t[2]) + "s"
    _msg = struct.unpack(fmt, serializeMessage)
    res = struct.unpack(_msg[3].decode("utf8"), _msg[4])
    for i in res:
        get_message.append(i)
    return get_message