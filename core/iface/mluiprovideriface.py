#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

class MLPluginUIProviderIFace:
    @abstractmethod
    def mlGetTrainerLoaderUI(self):
        raise NotImplementedError

    @abstractmethod
    def mlGetTrainerEditorUI(self):
        raise NotImplementedError

    @abstractmethod
    def mlGetNetworkDrawerUI(self):
        raise NotImplementedError
