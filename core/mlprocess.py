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

        self._shared['exit']      = False
        self._shared['running']   = False

    def mlGetUniqId(self):
        return self._uuid

    def mlPauseProcess(self):
        self._shared['running'] = False

    def mlResumeProcess(self):
        if not self._shared['exit']:
            self._shared['running'] = True

    def mlIsProcessRunning(self):
        ret = False
        if 'running' in self._shared.keys():
            ret = self._shared['running']
        return ret

    def mlIsProcessPaused(self):
        return not self.mlIsProcessRunning()

    def mlIsProcessExited(self):
        ret = False
        if 'exit' in self._shared.keys():
            ret = self._shared['exit']
        return ret

    def mlKillProcess(self):
        self._shared['exit'] = True
        self.terminate()
        self.join()

    def run(self):
        raise NotImplementedError
