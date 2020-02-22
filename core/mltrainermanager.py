#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.mlprocessmanager import MLProcessManager

import os

class MLTrainerManager(MLProcessManager):
    def __init__(self):
        MLProcessManager.__init__(self)

    def mlSaveProgression(self, directory):
        if os.path.exists(directory) and os.path.isdir(directory):
            trainer_directory = os.path.join(directory, 'trainers')
            if not os.path.exists(trainer_directory):
                os.mkdir(trainer_directory)

            for process in self._processes.values():
                if not process.mlIsProcessExited():
                    process.mlSaveTrainerProgression(trainer_directory)

    def mlRestoreProgression(self, directory, name, progress, error):
        if os.path.exists(directory) and os.path.isdir(directory):
            trainer_directory = os.path.join(directory, 'trainers')

            if os.path.exists(trainer_directory) and os.path.isdir(trainer_directory):
                for process in self._processes.values():
                    if process.mlGetUserName() == name and not process.mlIsProcessExited():
                        process.mlRestoreTrainerProgression(trainer_directory, progress, error)
                        break
