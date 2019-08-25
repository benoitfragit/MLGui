#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

class MLPluginUIProviderIFace:
    @abstractmethod
    def mlGetTrainerLoaderUI(self):
        raise NotImplementedError
