# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
command information
"""
__author__ = "jeremyjone"
__datetime__ = "2019/1/22 16:22"
__all__ = ["__version__", "DLConnect"]
__version__ = "1.0.0"
import Deadline.DeadlineConnect as Connect
from dateutil import parser

import connect
from config import DB, PARAM
import util


class DLConnect(object):
    def __init__(self):
        deadline_server = DB.DEADLINE_HOST
        deadline_port = DB.DEADLINE_PORT
        self.__deadline = Connect.DeadlineCon(deadline_server, deadline_port)

    @property
    def deadlineCon(self):
        return self.__deadline

    def submitTasks(self, message):
        job_info = message['JobInfo']
        plugin_info = message['PluginInfo']

        client_name = job_info[PARAM.NAME]
        respond_message = {PARAM.NAME: client_name}

        try:
            job = self.__deadline.Jobs.SubmitJob(job_info, plugin_info)
            respond_message['job_id'] = job['_id']
        except:
            util.JLOG.warning("Sorry, Web Service is currently down!")

        return respond_message, message["FileInfo"]

    def finishTasks(self, message, job_id, job_rmb):
        tasks = self.__deadline.Tasks.GetJobTasks(job_id)

        message['tasks'] = []
        info = "Billing details:\n"

        job_cost = 0
        total_time = 0.0
        for task in tasks['Tasks']:
            cpu_name = task['Slave']
            frame_number = task['Frames']
            start_time_str = task['StartRen']
            finish_time_str = task['Comp']

            start_time = parser.parse(start_time_str)
            finish_time = parser.parse(finish_time_str)
            used_time = finish_time - start_time

            cpu_info = self.__deadline.Slaves.GetSlaveInfo(cpu_name)
            core_count = cpu_info['Procs']

            # Calculate the cost for used time at each machine.
            # Core Count * RMB * Time(Hour) = Total Cost
            time_for_hour = used_time.total_seconds() / 3600.0
            task_cost = int(core_count) * job_rmb * time_for_hour
            job_cost += task_cost

            info += ('\t%s Core: %s,  Frame [%s] for Render Time : %s, '
                     'Task Cost: %f RMB\n' %
                     (cpu_name, core_count, frame_number, used_time, task_cost))

            task_data = {'frame': frame_number,
                         'slave_name': cpu_name,
                         'core_count': core_count,
                         'start_time': str(start_time),
                         'finish_time': str(finish_time),
                         'used_time': str(used_time),
                         'task_cost': task_cost}
            message['tasks'].append(task_data)

            total_time += used_time.total_seconds()

        util.JLOG.info(info)
        return job_cost, total_time, message

    def cancelTasks(self, message):
        job_id = message['job_id']

        try:
            job_result = self.__deadline.Jobs.FailJob(job_id)
            message['result'] = job_result
            util.JLOG.info(job_result)
        except:
            util.JLOG.warning("Sorry, Web Service is currently down!")

        return message

    def getSlaveInfo(self, poolName, key=None):
        res = []
        slaveName = self.__deadline.Slaves.GetSlaveNamesInPool(poolName)
        for i in range(len(slaveName)):
            slaveInfo = self.__deadline.Slaves.GetSlaveInfo(slaveName[i])
            if key:
                try:
                    slaveInfo = slaveInfo[key]
                except:
                    pass
            res.append(slaveInfo)
        return res
