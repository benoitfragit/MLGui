#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from iface import MLTrainerIFace
from mlprocess import MLProcess

class MLTrainer(MLProcess, MLTrainerIFace):
    def __init__(self, manager, plugin, internal, username):
        MLProcess.__init__(self, manager)

        self._internal  = internal
        self._plugin    = plugin
        self._username  = username

    def mlGetUserName(self):
        return self._username

    def mlDeleteTrainer(self):
        self._plugin.mlDeleteTrainer(self._internal)

    def mlConfigureTrainer(self, path):
        self._plugin.mlConfigureTrainer(self._internal, path)

    def mlIsTrainerRunning(self):
        return self._plugin.mlIsTrainerRunning(self._internal)

    def mlGetTrainerProgress(self):
        return self._plugin.mlGetTrainerProgress(self._internal)

    def mlTrainerRun(self):
        self.start()

    def mlGetTrainerError(self):
        return self._plugin.mlGetTrainerError(self._internal)

    def run(self):
        if 'running' not in self._shared.keys():
            self._shared['running']   = True
            self._shared['progress']  = self.mlGetTrainerProgress()
            self._shared['error']     = self.mlGetTrainerError()
            self._shared['pause']     = False
            self._shared['stopped']   = False
            self._shared['exit']      = False

        while (self._shared['running']):
            if self._shared['exit']:
                self._shared['stopped'] = True
                self._shared['running'] = False
            elif self._shared['pause']:
                self._resume.wait()
                self._resume.clear()
                self._shared['pause'] = False

            else:
                self._lock.acquire()
                self._plugin.mlTrainerRun(self._internal)
                self._lock.release()
                self._shared['running']   = self.mlIsTrainerRunning()
                self._shared['progress']  = self.mlGetTrainerProgress()
                self._shared['error']     = self.mlGetTrainerError()

        self._shared['exit'] = True

        print >>sys.stdout, 'Progress:%(prog)f, Error:%(err)f' % {'prog':self._shared['progress'], 'err':self._shared['error']}
