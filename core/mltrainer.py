#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from mlprocess import MLProcess
from mlnetworkprovider import MLNetworkProvider

class MLTrainer(MLProcess, MLNetworkProvider):
    def __init__(self, username, manager, plugin, internal):
        MLProcess.__init__(self, manager)
        network = plugin.mlTrainerGetManagedNetwork(internal)
        MLNetworkProvider.__init__(self, plugin, manager, network ,username, True)

        self._internal  = internal

        self._shared['running']   = False
        self._shared['exit']      = False
        self._shared['progress']  = 0.0;
        self._shared['error']     = 1.0;

    def mlGetPluginName(self):
        return self._plugin.mlGetPluginName()

    def mlIsPluginActivated(self):
        return self._plugin.mlIsPluginActivated()

    def mlDeleteTrainer(self):
        self._plugin.mlDeleteTrainer(self._internal)

    def mlConfigureTrainer(self, path):
        self._plugin.mlConfigureTrainer(self._internal, path)

    def mlIsTrainerRunning(self):
        return self._shared['running']

    def mlIsTrainerExited(self):
        return self._shared['exit']

    def mlGetTrainerProgress(self):
        return self._shared['progress']

    def mlTrainerRun(self):
        self.start()

    def mlGetTrainerError(self):
        return self._shared['error']

    def mlSetTrainerExited(self, exited):
        self._shared['exit'] = exited

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

                self.mlUpdateTrainerProvider()

                self._lock.release()

        self._shared['exit'] = True

    def mlSaveTrainerProgression(self, directory):
        path = os.path.join(directory, self._username)
        self._plugin.mlSaveTrainerProgression(self._internal, path)

    def mlRestoreTrainerProgression(self, directory, progress, error):
        path = os.path.join(directory, self._username)
        self._lock.acquire()
        self._plugin.mlRestoreTrainerProgression(self._internal, path, progress, error)
        self._lock.release()
        self._shared['progress'] = progress
        self._shared['error']    = error

    def mlJSONEncoding(self, d):
        username    = self.mlGetUserName()
        running     = self.mlIsTrainerRunning() > 0
        exited      = self.mlIsTrainerExited() > 0
        error       = self.mlGetTrainerError()
        progress    = self.mlGetTrainerProgress()

        d[username] = {}

        self._plugin.mlTrainerJSONEncoding(self._internal, d[username])

        d[username]['running']  = running
        d[username]['exit']     = exited
        d[username]['error']    = error
        d[username]['progress'] = progress

    def mlGetInternal(self):
        return self._internal

    def mlUpdateTrainerProvider(self):
        for i in self.arrays.keys():
            signal = None
            sizeOfSignal = len(self._arrays[i])
            if i == 0:
                signal = self._plugin.mlGetTrainerInputSignal(self._internal, sizeOfSignal)
            else:
                signal = self._plugin.mlGetTrainerLayerOutputSignal(self._internal, i - 1, sizeOfSignal)
            if signal is not None:
                self._arrays[i] = signal[:]
                print i, self._arrays[i]
