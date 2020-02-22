#!/usr/bin/env python
# -*- coding: utf-8 -*-

from iface.plugin import MLPluginIFace
import uuid

class MLPluginBase( MLPluginIFace):
    def __init__(self):
        self._uuid      = uuid.uuid4()
        self._activated         = False
        self._name              = None
        self._version           = None
        self._author            = None
        self._description       = None

    def mlGetUniqId(self):
        return self._uuid

    def mlSetPluginActivated(self, activated):
        self._activated = activated

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
