#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

from multiprocessing import Process
from multiprocessing import Event
from multiprocessing import Lock


class MLProcess(Process):
    def __init__(self, manager):
        Process.__init__(self)

        self._uuid = uuid.uuid4()
        self._lock = Lock()
        self._shared = manager.dict()

        self._shared['exit'] = False
        self._shared['running'] = False
        self._shared['paused'] = False
        self._shared['finished'] = False

    def mlGetUniqId(self):
        return self._uuid

    def mlPauseProcess(self):
        self._shared['paused'] = True

    def mlResumeProcess(self):
        self._shared['paused'] = False

    def mlIsProcessRunning(self):
        ret = False
        if 'running' in self._shared.keys():
            ret = self._shared['running']
        return ret

    def mlIsProcessPaused(self):
        return self._shared['paused']

    def mlIsProcessExited(self):
        ret = False
        if 'exit' in self._shared.keys():
            ret = self._shared['exit']
        return ret

    def mlIsProcessFinished(self):
        return self._shared['finished']

    def mlKillProcess(self):
        self._shared['exit'] = True
        self.terminate()
        self.join()

    def run(self):
        raise NotImplementedError
