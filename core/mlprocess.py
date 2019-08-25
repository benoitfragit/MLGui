#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

from multiprocessing import Process
from multiprocessing import Event
from multiprocessing import Lock

class MLProcess(Process):
    def __init__(self, manager):
        Process.__init__(self)

        self._uuid  = uuid.uuid4()
        self._lock  = Lock()
        self._shared= manager.dict()
        self._resume= Event()

        self._shared['pause']     = False
        self._shared['stopped']   = False
        self._shared['exit']      = False
        self._shared['running']   = False
        self._shared['progress']  = 0.0;
        self._shared['error']     = 1.0;

    def mlGetUniqId(self):
        return self._uuid

    def mlPauseProcess(self):
        self._shared['pause'] = True

    def mlResumeProcess(self):
        self._resume.set()

    def mlIsProcessRunning(self):
        ret = False
        if 'running' in self._shared.keys():
            ret = self._shared['running']
        return ret

    def mlIsProcessPaused(self):
        ret = False
        if 'pause' in self._shared.keys():
            ret = self._shared['pause'] and \
                  self._shared['running']
        return ret

    def mlIsProcessFinish(self):
        ret = False
        if 'exit' in self._shared.keys():
            ret = self._shared['exit']
        return ret

    def mlKillProcess(self):
        self._shared['exit'] = True
        self.terminate()
        self.join()
        self._shared['running'] = False

    def run(self):
        raise NotImplementedError
