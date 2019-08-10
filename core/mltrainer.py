#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Process
from iface import MLTrainerIFace

class MLTrainer(MLTrainerIFace, Process):
    def __init__(self, plugin, internal):
        Process.__init__(self)
        self._internal  = internal
        self._plugin    = plugin
        self._running   = False

    def mlDeleteTrainer(self):
        self._plugin.mlDeleteTrainer(self._internal)

    def mlConfigureTrainer(self, path):
        self._plugin.mlConfigureTrainer(self._internal, path)

    def mlIsTrainerRunning(self):
        return self._plugin.mlIsTrainerRunning(self._internal)

    def mlGetTrainerProgress(self):
        return self._plugin.mlGetTrainerProgress(self._internal)

    def mlTrainerRun(self):
        self._plugin.mlTrainerRun(self._internal)

    def mlGetTrainerError(self):
        return self._plugin.mlGetTrainerError(self._internal)

    def run(self):
        self._running = True
        while (self._running):
            self.mlTrainerRun()
            self._running = self.mlIsTrainerRunning()
