# !/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import datetime
import threading
import subprocess
from dateutil import parser

from config import PARAM
from connect import protocol
from connect.deadline_connect import DLConnect
import connect
from model.job_model import RenderJob
from database.db_handle import MangoDBHandle
import model
import widget
from util import handle
import util

class RenderClient(object):
    def __init__(self, UserName, isOnline=True):
        self.username = UserName
        self.ip = ""
        self.email = ""
        self.root_path = ""
        self.password = ""
        self.create_time = None
        self.last_login_time = None
        self.last_logout_time = None
        self.total_login_time = 0
        self.total_render_time = 0
        self.effective_render_time = 0
        self.unit_price = 0.05
        self.total_payed = 0.00
        self.total_render_cost = 0.00
        self.jobs = {}
        self.total_balance = 0.00
        self.recharge_record = []
        self.isvalid = True

        self.rendering_jobs = {}
        self.USER_INFO = None
        self._update_interval = 2  # Sleep time(s)
        self.job_window = None

        self.md = MangoDBHandle()

        # load user information
        self.initInfo()

        if isOnline:
            # Check job state, if start or queue, put to rendering_job dict.
            self.loadJob()

            # If job not finish, update information
            # self._update()

    def initInfo(self):
        user_info = self.md.getUserInfo(self.username)
        self.USER_INFO = user_info
        """
        user_info format:
        
        {u'CreateDate': datetime.datetime(2019, 2, 2, 3, 27, 37, 621000),
         u'EffectiveRenderTime': 0,
         u'Email': u'',
         u'IP': u'192.168.1.4',
         u'JobCompleted': True,
         u'JobFailed': True,
         u'JobTaskTimeout': True,
         u'JobWarning': True,
         u'LastLoginTime': datetime.datetime(2019, 2, 28, 2, 56, 13, 213000),
         u'LastLogoutTime': datetime.datetime(2019, 2, 13, 10, 42, 11, 745000),
         u'Machine': u'',
         u'MyJobs': [u'5c550e7ec3a4c52f909910c9'],
         u'Name': u'jztest',
         u'Password': u'123',
         u'RunAsDom': u'',
         u'RunAsHash': u'',
         u'RunAsName': u'',
         u'SendEmail': False,
         u'SendPopup': False,
         u'Service': u'',
         u'SvcHash': None,
         u'TotalLoginTime': 0,
         u'TotalPayed': 0.0,
         u'TotalRenderCost': 0.0,
         u'TotalRenderTime': 17.078,
         u'UnitPrice': 0.05,
         u'RechargeRecord': 
            [{
                u'Date': datetime.datetime(2019, 2, 13, 10, 41, 12, 367000), 
                u'Money': 120.00,
             },
             {...},
            ],
         u'TotalBalance': 111.27,
         u'IsValid': True,
         '_id': u'jztest'}
        """
        # Create user root path, ftp root + username
        self.root_path = os.path.join(model.DB_CONFIGURE.ftpPath, self.username)

        if user_info.get(u'IsValid') == False:
            self.isvalid = False

        if user_info.get(u'IP') != None:
            self.ip = user_info.get(u'IP')

        if user_info.get(u'Email') != None:
            self.email = user_info.get(u'Email')

        if user_info.get(u'Password') != None:
            self.password = user_info.get(u'Password')

        if user_info.get(u'UnitPrice') != None:
            self.unit_price = user_info.get(u'UnitPrice')

        if user_info.get(u'TotalPayed') != None:
            self.total_payed = user_info.get(u'TotalPayed')

        if user_info.get(u'TotalRenderCost') != None:
            self.total_render_cost = user_info.get(u'TotalRenderCost')

        if user_info.get(u"TotalBalance") != None:
            self.total_balance = user_info.get(u"TotalBalance")

        if user_info.get(u"RechargeRecord"):
            self.recharge_record = user_info.get(u"RechargeRecord")

        # Second time, use it need transform 00:00:00 format, (handle.formatTime)
        if user_info.get(u'TotalLoginTime') != None:
            self.total_login_time = user_info.get(u'TotalLoginTime')
        if user_info.get(u'TotalRenderTime') != None:
            self.total_render_time = user_info.get(u'TotalRenderTime')
        if user_info.get(u'EffectiveRenderTime') != None:
            self.effective_render_time = user_info.get(u'EffectiveRenderTime')

        # Datetime object, need to transform to str
        if user_info.get(u'CreateDate') != None:
            self.create_time = handle.date2str(user_info.get(u'CreateDate'))
        if user_info.get(u'LastLoginTime') != None:
            self.last_login_time = handle.date2str(user_info.get(u'LastLoginTime'))
        if user_info.get(u'LastLogoutTime') != None:
            self.last_logout_time = handle.date2str(user_info.get(u'LastLogoutTime'))

        # Create all job dict for user
        if user_info.get(u'MyJobs') != None:
            for job_id in user_info.get(u'MyJobs'):
                try:
                    self.jobs.update({job_id: RenderJob(job_id, self.username, self)})
                except Exception as e:
                    pass # should be pop this job from db document.  // later write.
                    util.JLOG.error("create job error, id: %s, error: %s" % (job_id, e))

    def _update(self):
        # self._timer = threading.Timer(self._update_interval, self._update)
        # self._timer.start()

        for job in self.rendering_jobs.values():
            # job_info = self.md.getJobInfo(job.id)
            # job.updateInfo(job_info)

            print "=======Check State=======", job.id, job.state, job.progress, job._check_start_flag
            # if job.state in [model.STATE.Start.value, model.STATE.Queue.value]:
            #     if job._check_start_flag:
            #         self.clientJobStart(job)
            #         job._check_start_flag = False
            #
            #     if job.errors > 0:
            #         err_msg = {"job_id": job.id, "Errs": job.errors}
            #         connect.sendMessageByName(self.username,
            #                                   protocol.MessageType.send_error_count_from_server,
            #                                   err_msg
            #                                   )
            #
            #     # job.progress = int((job.completed_chunks / float(job.tasks)))
            #     # self.md.saveJobInfo(job.id, {"CompProgress": job.progress})
            #     job.updateInfo()
            #     job.saveCompProgress(int((job.completed_chunks / float(job.tasks)) * 100))
            #     print "progress:", job.progress, job.completed_chunks, job.tasks
            #     message = {u'UserName': self.username,
            #                u'job_id': job.id,
            #                u'complete': str(job.progress),
            #                }
            #
            #     connect.sendMessageByName(self.username,
            #                               protocol.MessageType.render_progress,
            #                               message
            #                               )
            #
            # elif job.state == model.STATE.Finish.value:
            #     self.clientJobFinish(job)
            #     self.rendering_jobs.pop(job.id)
            #     widget.JWindow.FINISH_SIGNAL.emit(job)
            #
            # elif job.state == model.STATE.Error.value:
            #     self.clientJobError(job)
            #     self.rendering_jobs.pop(job.id)
            #     widget.JWindow.CANCEL_SIGNAL.emit({"UserName": job.username, "job_id": job.id})
            #
            # widget.JWindow.UPDATE_SIGNAL.emit(job)

    def destroy(self):
        # self._timer.cancel()
        if self.job_window != None:
            self.job_window.close()

    def checkLogin(self, data):
        if all([
            # === If has more login check rule, append to this list. ===
            data.get("PassWord") == self.password, # same password
            self.isvalid, # valid username
            data[PARAM.NAME].lower() not in PARAM.ADMIN_LIST, # username not admin name
       ]):
            return True
        return False

    def loadJob(self):
        for job in self.jobs.values():
            if job.state in [model.STATE.Start.value,
                             model.STATE.Queue.value]:  # Active job state
                # self.rendering_jobs.update({job.id: job})
                handle.checkDB(self.username, job.id)

            # check Job CompProgress and save to database.
            if job.progress != 100 and job.completed_chunks != job.tasks:
                # info = {"CompProgress": int((job.completed_chunks / float(job.tasks)) * 100)}
                # self.md.saveJobInfo(job.id, info)
                job.saveCompProgress(int((job.completed_chunks / float(job.tasks)) * 100))

            if job.state == model.STATE.Finish.value and \
                    not any([job.render_time, job.cost]):
                self.finishHandle(job.id)

    def createJob(self, job_id):
        self.jobs.update({job_id: RenderJob(job_id, self.username, self)})
        # self.rendering_jobs.update({job_id: RenderJob(job_id, self.username)})
        handle.checkDB(self.username, job_id)
        self.saveInfo()

    # def updateInfo(self, job_id):
    #     '''{u'UserName': u'jztest3', u'Progress': u'100', u'State': u'3', u'Errors': u'0', u'Job_id': u'5c91f5a9c3a4c52304c1fc80'}'''

        # if job.state in [model.STATE.Start.value, model.STATE.Queue.value]:
        #     if job._check_start_flag:
        #         self.clientJobStart(job)
        #         job._check_start_flag = False
        #
        #     if job.errors > 0:
        #         err_msg = {"job_id": job.id, "Errs": job.errors}
        #         connect.sendMessageByName(self.username,
        #                                   protocol.MessageType.send_error_count_from_server,
        #                                   err_msg
        #                                   )
        #
        #     # job.progress = int((job.completed_chunks / float(job.tasks)))
        #     # self.md.saveJobInfo(job.id, {"CompProgress": job.progress})
        #     job.updateInfo()
        #     job.saveCompProgress(int((job.completed_chunks / float(job.tasks)) * 100))
        #     print "progress:", job.progress, job.completed_chunks, job.tasks
        #     message = {u'UserName': self.username,
        #                u'job_id': job.id,
        #                u'complete': str(job.progress),
        #                }
        #
        #     connect.sendMessageByName(self.username,
        #                               protocol.MessageType.render_progress,
        #                               message
        #                               )
        #
        # elif job.state == model.STATE.Finish.value:
        #     self.clientJobFinish(job)
        #     self.rendering_jobs.pop(job.id)
        #     widget.JWindow.FINISH_SIGNAL.emit(job)
        #
        # elif job.state == model.STATE.Error.value:
        #     self.clientJobError(job)
        #     self.rendering_jobs.pop(job.id)
        #     widget.JWindow.CANCEL_SIGNAL.emit({"UserName": job.username, "job_id": job.id})
        #
        # widget.JWindow.UPDATE_SIGNAL.emit(job)

    def saveInfo(self):
        info = {u'EffectiveRenderTime': self.effective_render_time,
                u'Email': self.email,
                u'IP': self.ip,
                u'MyJobs': self.jobs.keys(),
                u'Name': self.username,
                u'Password': self.password,
                u'TotalLoginTime': self.total_login_time,
                u'TotalPayed': self.total_payed,
                u'TotalRenderCost': self.total_render_cost,
                u'TotalRenderTime': self.total_render_time,
                u'UnitPrice': self.unit_price,
                u'_id': self.username,
                u'LastLoginTime': handle.str2date(self.last_login_time),
                u'LastLogoutTime': handle.str2date(self.last_logout_time),
                u'TotalBalance': self.total_balance,
                u'RechargeRecord': self.recharge_record,
                u'IsValid': self.isvalid,
                }
        self.USER_INFO.update(info)
        self.md.saveUser(self.USER_INFO)
        self.last_login_time = handle.date2str(self.last_login_time)
        self.last_logout_time = handle.date2str(self.last_logout_time)

    # def saveRechargeInfo(self, money, **kwargs):
    #     self.total_balance += money
    #     recharge_info = {
    #         u"Money": money,
    #     }
    #     recharge_info.update(kwargs)
    #     self.recharge_record.append(recharge_info)
    #
    #     info = {
    #         u'TotalBalance': self.total_balance,
    #         u'RechargeRecord': self.recharge_record,
    #     }
    #     print info
    #     self.md.saveUserInfo(self.username, info)
    #     self.USER_INFO.update(info)

    @property
    def getUserInfo(self):
        info = {
            "TotalPayed": self.total_payed,
            "TotalRenderCost": self.total_render_cost,
            "TotalRenderTime": self.total_render_time,
            "TotalBalance": self.total_balance,
        }
        return info

    def getJobInfo(self):
        job_list = []
        for job in self.jobs.values():
            job_list.append(job.jobInfo)
        return job_list

    def saveUsedTime(self, job):
        # Save EndTime to Job
        compTime = parser.parse(handle.getUTCDate().__str__())
        start_time = parser.parse(handle.str2date(job.start_time).__str__())
        used_time = (compTime - start_time).total_seconds()
        if handle.str2date(job.start_time) < datetime.datetime.fromtimestamp(0):
            used_time = 0

        self.md.updateUserInfo(self.username, "TotalRenderTime", used_time)
        # self.md.saveJobInfo(job.id, {"DateComp": compTime, "RenderTime": used_time})
        job.saveDateComp(compTime)
        job.saveRenderTime(used_time)

    def submitHandle(self, data):
        dl = DLConnect()
        respond_message, file_info = dl.submitTasks(data)
        # save FileInfo to database.
        self.md.saveJobInfo(respond_message['job_id'], {"FileInfo": file_info})
        self.clientJobSubmit(respond_message)

    def finishHandle(self, job_id, message=None):
        dl = DLConnect()
        self.jobs[job_id].updateInfo()

        if not message:
            message = dl.deadlineCon.Jobs.GetJob(job_id)
            message.update({"UserName": self.username})

        job_cost, used_time, message = dl.finishTasks(message, job_id, self.unit_price)
        # print ('Job ID: %s, Total Job Cost: %f RMB' % (job_id, job_cost))
        message['job_cost'] = job_cost
        # info = {"Cost": job_cost, "PayState": False, "RenderTime": used_time, "CompProgress": 100}

        # self.md.saveJobInfo(job_id, info)
        self.jobs[job_id].saveCost(job_cost)
        self.jobs[job_id].savePayState(False)
        self.jobs[job_id].saveRenderTime(used_time)
        self.jobs[job_id].saveCompProgress(100)

        self.md.updateUserInfo(self.username, "TotalRenderCost", job_cost)
        self.md.updateUserInfo(self.username, "TotalRenderTime", used_time)
        self.md.updateUserInfo(self.username, "EffectiveRenderTime", used_time)

    def cancelHandle(self, job):
        dl = DLConnect()
        job.updateInfo()
        job_data = job.JOB_INFO
        job_data.update({"job_id": job.id})
        message = dl.cancelTasks(job_data)
        self.clientJobCancel(message)

    def clientJobSubmit(self, message):
        job_id = message['job_id']
        self.createJob(job_id)

        # Save job to UserInfo
        self.md.addJob2User(self.username, job_id)

        # dl = DLConnect()
        # job_info = dl.deadlineCon.Jobs.GetJob(job_id)
        # job_info.update({"UserName": self.username})

        job = self.jobs[job_id]

        # job.saveJobState(model.STATE.Start.value)

        # info = {"Cost": 0.0,
        #         "PayState": False,
        #         "RenderTime": 0,
        #         "CompProgress": 0,
        #         "DateStart": handle.getUTCDate()
        #         }
        # self.md.saveJobInfo(job.id, info)
        job.saveCost(0.0)
        job.savePayState(False)
        job.saveRenderTime(0)
        job.saveCompProgress(0)

        # message: {"UserName": username, "job_id": id}
        try:
            local_submit_time = handle.getLocalDate(job.submit_time)
            submit_time = local_submit_time.strftime('%Y-%m-%d %H:%M:%S')
        except:
            submit_time = ""

        message.update({
            u"SubmitDate": submit_time,
        })

        connect.sendMessageByName(self.username,
                                  protocol.MessageType.render_submit,
                                  message
                                  )
        widget.JWindow.JOB_SUBMIT_SIGNAL.emit(self.jobs[job_id])

    def clientJobStart(self, job):
        send_message = {}
        send_message["job_id"] = job.id

        job.saveJobState(model.STATE.Start.value)

        # info = {"Cost": 0.0,
        #         "PayState": False,
        #         "RenderTime": 0,
        #         "CompProgress": 0,
        #         "DateStart": handle.getUTCDate()
        #         }
        # self.md.saveJobInfo(job.id, info)
        job.saveCost(0.0)
        job.savePayState(False)
        job.saveRenderTime(0)
        job.saveCompProgress(0)
        job.saveDateStart(handle.getUTCDate())

        local_start_time = handle.getLocalDate(job.start_time)
        start_time = local_start_time.strftime('%Y-%m-%d %H:%M:%S')
        send_message.update({
            u"StartDate": start_time,
        })

        connect.sendMessageByName(self.username,
                                  protocol.MessageType.render_start,
                                  send_message
                                  )
        widget.JWindow.UPDATE_SIGNAL.emit(job)

    def clientJobFinish(self, job):
        message = job.JOB_INFO
        message.update({"job_id": job.id})

        # job.state = model.STATE.Finish.value
        # job.saveCompProgress(100)

        # connect.sendMessageByName(self.username,
        #                           protocol.MessageType.render_progress,
        #                           {u'UserName': self.username, u'job_id': job.id, u'complete': u"100"}
        #                           )
        self.finishHandle(job.id, message)

        msg = self.jobs[job.id].jobInfo
        msg.update({"job_id": job.id})
        connect.sendMessageByName(self.username,
                                  protocol.MessageType.render_finish,
                                  msg
                                  )
        widget.JWindow.UPDATE_SIGNAL.emit(job)

    def clientJobCancel(self, message):
        try:
            job_id = message['job_id']
        except:
            job_id = message["_id"]
            message.update({"job_id": job_id})

        self.jobs[job_id].saveJobState(model.STATE.Error.value)
        self.jobs[job_id].updateInfo()

        self.saveUsedTime(self.jobs[job_id])
        msg = self.jobs[job_id].jobInfo
        msg.update({"job_id": job_id})
        msg.update({"result": message["result"]})
        connect.sendMessageByName(self.username,
                                  protocol.MessageType.render_cancel,
                                  msg
                                  )
        widget.JWindow.UPDATE_SIGNAL.emit(self.jobs[job_id])

    def clientJobError(self, job):
        message = job.JOB_INFO
        message.update({"job_id": job.id})

        # job.updateInfo()
        job.saveJobState(model.STATE.Error.value)

        self.saveUsedTime(job)
        msg = job.jobInfo
        msg.update({"job_id": job.id})

        connect.sendMessageByName(self.username,
                                  protocol.MessageType.render_error,
                                  msg
                                  )
        widget.JWindow.UPDATE_SIGNAL.emit(job)

