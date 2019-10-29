#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

class MLNetwork:
    def __init__(self, username, plugin, internal, managed = False):
        self._plugin = plugin
        self._internal = internal
        self._username = username
        self._uuid  = uuid.uuid4()
        self._managed = managed

    def mlIsManaged(self):
        return self._managed

    def mlGetUserName(self):
        return self._username

    def mlGetUniqId(self):
        return self._uuid

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

    def mlGetNetworkDrawerUI(self):
        return self._plugin.mlGetNetworkDrawerUI()

    def mlDisplayNetworkDrawerUI(self):
        scene = self.mlGetNetworkDrawerUI()

        # clear the scene
        scene.clear()

        # draw the scene
        scene.mlOnDisplayNetwork(self._internal)
