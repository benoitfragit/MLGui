#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MLTrainerIFace:
    def mlDeleteTrainer(self):
        raise NotImplementedError

    def mlConfigureTrainer(self, path):
        raise NotImplementedError

    def mlIsTrainerRunning(self):
        raise NotImplementedError

    def mlGetTrainerProgress(self):
        raise NotImplementedError

    def mlTrainerRun(self):
        raise NotImplementedError

    def mlGetTrainerError(self):
        raise NotImplementedError
