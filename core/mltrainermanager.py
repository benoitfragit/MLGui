#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mlprocessmanager import MLProcessManager

class MLTrainerManager(MLProcessManager):
    def __init__(self):
        MLProcessManager.__init__(self)
        self._trainers = {}

    def mlAddTrainer(self, trainer):
        if trainer is not None :
            uuid = trainer.mlGetUniqId()
            if uuid not in self._trainers.keys():
                self._trainers[uuid] = trainer

    def mlStartTrainerWithId(self, uuid):
        if uuid in self._trainers.keys():
            self.mlNewProcess(self._trainers[uuid])

    def mlStopTrainerWithId(self, uuid):
        if uuid in self._trainers.keys():
            self.mlKillWithId(self._trainers[uuid])

    def mlPauseTrainerWithId(self, uuid):
        if uuid in self._trainers.keys():
            self._processmanager.mlPauseProcess(uuid)

    def mlResumeTrainerWithId(self, uuid):
        if uuid in self._trainers.keys():
            self.mlResumeProcess(uuid)

    def mlRemoveTrainerWithId(self, uuid):
        if uuid in self._trainers.keys():
            """
            First stop any running process
            """
            self.mlKillWithId(uuid)
            self._trainers.pop(uuid)
