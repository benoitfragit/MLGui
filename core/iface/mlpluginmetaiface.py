#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

class MLPluginMetaDataIFace:
    @abstractmethod
    def mlGetPluginName(self):
        raise NotImplementedError

    @abstractmethod
    def mlGetPluginAuthor(self):
        raise NotImplementedError

    @abstractmethod
    def mlGetPluginVersion(self):
        raise NotImplementedError

    @abstractmethod
    def mlGetPluginDescription(self):
        raise NotImplementedError
