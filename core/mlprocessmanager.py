#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing.managers import SyncManager

import sys

class MLProcessManager(SyncManager):
    def __init__(self):
        SyncManager.__init__(self)
        self.start()
        self._processes = {}

    def mlKillProcessWithId(self, id):
        if id in self._processes.keys():
            self._processes[id].mlKillProcess()

    def mlKillAll(self):
        for id in self._processes.keys():
            self.mlKillProcessWithId(id)

    def mlPauseProcess(self, id):
        if id in self._processes.keys():
            self._processes[id].mlPauseProcess()

    def mlResumeProcess(self, id):
        if id in self._processes.keys():
            self._processes[id].mlResumeProcess()

    def mlAddProcess(self, p):
        id = p.mlGetUniqId()
        if id not in self._processes.keys():
            self._processes[id] = p

    def mlStartProcess(self, id):
        if id in self._processes.keys():
            self._processes[id].start()

    def mlRemoveProcess(self, id):
        if id in self._processes.keys():
            self._processes[id].mlKillProcess()
            self._processes.pop(id)

    def mlIsProcessRunning(self, id):
        ret = False
        if id in self._processes.keys():
            ret = self._processes[id].mlIsProcessRunning()
        return ret

    def mlIsProcessPaused(self, id):
        ret = False
        if id in self._processes.keys():
            ret = self._processes[id].mlIsProcessPaused()
        return ret
