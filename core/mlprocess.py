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
        self._pause = Event()
        self._resume= Event()
        self._quit  = Event()

    def mlGetUniqId(self):
        return self._uuid

    def mlPauseProcess(self):
        self._pause.set()

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

    def mlKillProcess(self):
        self._quit.set()
        self.terminate()
        self.join()

    def run(self):
        raise NotImplementedError
