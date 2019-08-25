#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

class MLPluginActivableIFace:
    @abstractmethod
    def mlSetPluginActivated(self, activated):
        raise NotImplementedError

    @abstractmethod
    def mlIsPluginActivated(self):
        raise NotImplementedError
