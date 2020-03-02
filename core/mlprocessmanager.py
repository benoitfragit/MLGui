#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing.managers import SyncManager

import sys


class MLProcessManager(SyncManager):
    def __init__(self):
        SyncManager.__init__(self)
        self.start()
        self._processes = {}

    def mlKillAll(self):
        for id in self._processes.keys():
            self._processes[id].mlKillProcess()

    def mlAddProcess(self, p):
        id = p.mlGetUniqId()
        if id not in self._processes.keys():
            self._processes[id] = p

    def mlRemoveProcess(self, id):
        if id in self._processes.keys():
            self._processes.pop(id)
