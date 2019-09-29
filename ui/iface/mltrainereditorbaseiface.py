#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

class MLTrainerEditorBaseIface:
    @abstractmethod
    def mlBuildTrainerEditorMainWidget(self):
        raise NotImplementedError

    @abstractmethod
    def fromTrainer(self, *args, **kwargs):
        raise NotImplementedError
