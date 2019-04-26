# !/usr/bin/env python
# -*- coding:utf-8 -*-

from threading import Thread
import time
from dateutil import parser
import datetime


def formatTime(time):
    if time and isinstance(time, float) or isinstance(time, int):
        h = int(time / 3600.0)
        m = int(time % 3600.0 / 60.0)
        s = int(time % 60.0)
        return "%02d:%02d:%02d" % (h, m, s)
    return "00:00:00"

def get_localdate(str_date, timedelta=8):
    _date = parser.parse(str_date)
    return _date + datetime.timedelta(hours=timedelta)


class LogonTimerThread(Thread):
    def __init__(self, event, update_time_signal):
        Thread.__init__(self)
        self.UPDATE_TIME_SIGNAL = update_time_signal
        self.stopped = event
        self._update_interval = 1.0
        self.start_time = datetime.datetime.now()

    def run(self):
        while not self.stopped.wait(self._update_interval):

            end = datetime.datetime.now()
            elapsed = end - self.start_time
            time_format = parser.parse(str(elapsed)).strftime("%H:%M:%S")
            self.UPDATE_TIME_SIGNAL.emit(time_format)