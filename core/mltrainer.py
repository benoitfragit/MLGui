#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from iface import MLTrainerIFace
from mlprocess import MLProcess

class MLTrainer(MLProcess, MLTrainerIFace):
    def __init__(self, manager, plugin, network_filepath, data_filepath, username):
        MLProcess.__init__(self, manager)

        self._internal  = plugin.mlGetTrainer(network_filepath, data_filepath)
        self._plugin    = plugin
        self._username  = username

        self._shared['running']   = False
        self._shared['progress']  = self.mlGetTrainerProgress()
        self._shared['error']     = self.mlGetTrainerError()

    def mlGetUserName(self):
        return self._username

    def mlDeleteTrainer(self):
        self._plugin.mlDeleteTrainer(self._internal)

    def mlConfigureTrainer(self, path):
        self._plugin.mlConfigureTrainer(self._internal, path)

    def mlIsTrainerRunning(self):
        return self._shared['running']

    def mlGetTrainerProgress(self):
        return self._shared['progress']

    def mlTrainerRun(self):
        self.start()

    def mlGetTrainerError(self):
        return self._shared['error']

    def run(self):
        self._shared['running']   = True
        self._shared['progress']  = self.mlGetTrainerProgress()
        self._shared['error']     = self.mlGetTrainerError()

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
                self._shared['running']   = self._plugin.mlIsTrainerRunning(self._internal)
                self._shared['progress']  = self._plugin.mlGetTrainerProgress(self._internal)
                self._shared['error']     = self._plugin.mlGetTrainerError(self._internal)
                self._lock.release()

        self._shared['exit'] = True
