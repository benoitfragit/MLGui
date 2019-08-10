#!/usr/bin/env python
# -*- coding: utf-8 -*-

from iface import MLPluginActivableIFace
from iface import MLPluginMetaDataIFace
from iface import MLPluginIFace

class MLPluginBase( MLPluginIFace, \
                    MLPluginActivableIFace, \
                    MLPluginMetaDataIFace):
    def __init__(self):
        self._activated = False
        self._name = None
        self._version = None
        self._author = None
        self._description = None

    def mlIsPluginActivated(self):
        return self._activated

    def mlGetPluginName(self):
        return self._name

    def mlGetPluginAuthor(self):
        return self._author

    def mlGetPluginDescription(self):
        return self._description

    def mlGetPluginVersion(self):
        return self._version
