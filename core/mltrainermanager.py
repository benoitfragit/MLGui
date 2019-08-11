#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MLTrainerManager:
    def __init__(self, args):
        self._processmanager = args
        self._trainers = {}

    def mlAddTrainer(self, trainer):
        if trainer is not None :
            uuid = trainer.mlGetUniqId()
            if uuid not in self._trainers.keys():
                self._trainer[uuid] = trainer

    def mlStartTrainerWithId(self, uuid):
        if uuid in self._trainers.keys():
            self._processmanager.mlNewProcess(self._trainers[uuid])

    def mlStopTrainerWithId(self, uuid):
        if uuid in self._trainers.keys():
            self._processmanager.mlKillWithId(self._trainers[uuid])

    def mlPauseTrainerWithId(self, uuid):
        if uuid in self._trainers.keys():
            self._processmanager.mlPauseProcess(uuid)

    def mlResumeTrainerWithId(self, uuid):
        if uuid in self._trainers.keys():
            self._processmanager.mlResumeProcess(uuid)

    def mlRemoveTrainerWithId(self, uuid):
        if uuid in self._trainers.keys():
            """
            First stop any running process
            """
            self._processmanager.mlKillWithId(uuid)
            self._trainers.pop(uuid)
