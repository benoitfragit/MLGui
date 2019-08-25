#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

class MLTrainerIFace:
    @abstractmethod
    def mlDeleteTrainer(self):
        raise NotImplementedError

    @abstractmethod
    def mlConfigureTrainer(self, path):
        raise NotImplementedError

    @abstractmethod
    def mlIsTrainerRunning(self):
        raise NotImplementedError

    @abstractmethod
    def mlGetTrainerProgress(self):
        raise NotImplementedError

    @abstractmethod
    def mlTrainerRun(self):
        raise NotImplementedError

    @abstractmethod
    def mlGetTrainerError(self):
        raise NotImplementedError
