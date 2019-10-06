#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MLNetwork:
    def __init__(self, plugin, internal):
        self._plugin = plugin
        self._internal = internal

    def mlDeleteNetwork(self):
        self._plugin.mlDeleteNetwork(self._internal)

    def mlSaveNetwork(self, path):
        self._plugin.mlSaveNetwork(self._internal, path)

    def mlLoadNetwork(self, path):
        self._plugin.mlLoadNetwork(self._internal, path)

    def mlPredict(self, num, sig):
        self._plugin.mlPredict(self._internal, num, sig)

    def mlGetNetworkOutputLength(self):
        return self._plugin.mlGetNetworkOutputLength(self._internal)

    def mlGetNetworkPrediction(self):
        return self._plugin.mlGetNetworkPrediction(self._internal)
