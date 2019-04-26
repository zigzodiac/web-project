# !/usr/bin/env python
# -*- coding:utf-8 -*-
import model
from connect.deadline_connect import DLConnect
from database.db_handle import MangoDBHandle

import widget
import time
import connect
from connect import protocol
from util import handle


class RenderJob(object):
    def __init__(self, id, name, client):
        self._check_start_flag = True
        self.client = client

        self.id = id
        self.username = name
        self.state = model.STATE.Finish.value
        self.comment = None
        self.job_name = None
        self.submit_time = None
        self.start_time = None
        self.complete_time = None
        self.errors = 0
        self.render_time = 0
        self.pay_state = False
        self.scene_file = None
        self.cost = 0.00
        self.out_dir = None
        self.tasks = 0
        self.file_info = None
        self.plug_info = None
        self.pool = None
        self.progress = 0
        self.completed_chunks = 0

        self.md = MangoDBHandle()
        self.JOB_INFO = self.md.getJobInfo(self.id)

        self.updateInfo(self.JOB_INFO)

    def updateInfo(self, job_info=None):
        if not job_info:
            self.JOB_INFO = self.md.getJobInfo(self.id)
            job_info = self.JOB_INFO

        # Datetime format, need transform to str
        self.submit_time = handle.date2str(job_info[u'Date'])
        self.start_time = handle.date2str(job_info[u'DateStart'])
        self.complete_time = handle.date2str(job_info[u'DateComp'])

        # a number, transform to STATE enum class
        self.state = job_info[u'Stat']

        self.job_name = job_info[u'Props'][u'Name']
        self.comment = job_info[u'Props'][u'Cmmt']
        self.errors = job_info[u'Errs']
        self.render_time = job_info.get(u'RenderTime')
        self.pay_state = job_info.get(u'PayState')
        self.out_dir = job_info[u'OutDir']
        self.tasks = job_info[u'Props'][u'Tasks']
        self.scene_file = job_info[u"Props"][u"PlugInfo"][u"SceneFile"]
        self.file_info = job_info[u'FileInfo']  # list
        self.plug_info = job_info[u'Props'][u'PlugInfo']  # dict
        self.pool = job_info[u'Props'][u'Pool']
        self.progress = job_info.get(u'CompProgress')
        self.completed_chunks = job_info[u'CompletedChunks']
        _cost = job_info.get(u'Cost')
        self.cost = _cost if _cost else 0.00

    def update2user(self, job_info):
        self.progress = int(job_info["Progress"])
        self.state = int(job_info["State"])
        self.errors = int(job_info["Errors"])
        self.start_time = handle.date2str(handle.getLocalDate(job_info["StartDate"], 0))

        widget.JWindow.UPDATE_SIGNAL.emit(self)

        try:
            local_start_time = handle.getLocalDate(self.start_time)
            start_time = local_start_time.strftime('%Y-%m-%d %H:%M:%S')
        except:
            start_time = ""

        message = {u'UserName': self.username,
                   u'job_id': self.id,
                   u'complete': str(self.progress),
                   u"StartDate": start_time,
                   }

        connect.sendMessageByName(self.username,
                                  protocol.MessageType.render_progress,
                                  message
                                  )
        widget.JWindow.UPDATE_SIGNAL.emit(self)

        if self.errors > 0:
            err_msg = {"job_id": self.id, "Errs": self.errors}
            connect.sendMessageByName(self.username,
                                      protocol.MessageType.send_error_count_from_server,
                                      err_msg
                                      )

        if self.state == model.STATE.Finish.value:
            self.client.clientJobFinish(self)
            widget.JWindow.FINISH_SIGNAL.emit(self)

        if self.state == model.STATE.Error.value:
            self.client.clientJobError(self)
            widget.JWindow.CANCEL_SIGNAL.emit({"UserName": self.username, "job_id": self.id})

    # def saveJob(self):
    #     info = {
    #         u'RenderTime': self.render_time,
    #         u'PayState': self.pay_state,
    #         u'Cost': self.cost,
    #         u'CompProgress': self.progress,
    #     }
    #
    #     self.JOB_INFO.update(info)
    #     self.md.saveJobInfo(self.id, self.JOB_INFO)

    def saveRenderTime(self, renderTime):
        self.render_time = renderTime
        self.md.saveJobInfo(self.id, {"RenderTime": renderTime})

    def savePayState(self, state):
        self.pay_state = state
        self.md.saveJobInfo(self.id, {"PayState": state})

    def saveCost(self, cost):
        self.cost = cost
        self.md.saveJobInfo(self.id, {"Cost": cost})

    def saveCompProgress(self, progress):
        self.progress = progress
        self.md.saveJobInfo(self.id, {"CompProgress": progress})

    def saveDateStart(self, _date):
        self.start_time = handle.date2str(_date)
        self.md.saveJobInfo(self.id, {"DateStart": _date})

    def saveDateComp(self, _date):
        self.complete_time = handle.date2str(_date)
        self.md.saveJobInfo(self.id, {"DateComp": _date})

    def saveJobState(self, _date):
        self.state = _date
        self.md.saveJobInfo(self.id, {"Stat": _date})

    @property
    def jobInfo(self):
        _info = {
            "_id": self.id,
            "Date": self.submit_time,
            "DateStart": self.start_time,
            "DateComp": self.complete_time,
            "OutDir": self.out_dir,
            "Errs": self.errors,
            "Stat": self.state,
            "FileInfo": self.file_info,
            "Props": {
                "Name": self.job_name,
                "Cmmt": self.comment,
                "Frames": self.JOB_INFO["Props"]["Frames"],
                "PlugInfo": {
                    "SceneFile": self.scene_file,
                    "Camera": self.JOB_INFO["Props"]["PlugInfo"].get("Camera"),
                    "Renderer": self.JOB_INFO["Props"]["PlugInfo"].get("Renderer"),
                    "OutputDriver": self.JOB_INFO["Props"]["PlugInfo"].get("OutputDriver"),
                    "Version": self.JOB_INFO["Props"]["PlugInfo"]["Version"],
                }
            },
            "RenderTime": self.render_time,
            "PayState": self.pay_state,
            "CompProgress": self.progress,
            "Cost": self.cost,
        }

        return _info

    def getErrorInfo(self):
        info = self.md.getJobReport(self.id)

        err_list = []
        for error in info:
            if error["Type"] != 0:
                err_info = {"Date": handle.date2str(error.get("Date")),
                            "Type": error.get("Type"),
                            "Title": error.get("Title"),
                            "JobName": error.get("JobName"),
                            "Frames": error.get("Frames"),
                            }
                err_list.append(err_info)

        return err_list