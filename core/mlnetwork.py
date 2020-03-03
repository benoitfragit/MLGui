#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

from mlnetworkprovider import MLNetworkProvider


class MLNetwork(MLNetworkProvider):
    """

    """
    def __init__(self, username, plugin, internal):
        MLNetworkProvider.__init__(self, plugin, manager, internal, username, False)
        self._internal = internal
        self._uuid = uuid.uuid4()

    def mlGetUniqId(self):
        """

        @return:
        """
        return self._uuid

    def mlDeleteNetwork(self):
        """

        """
        self._plugin.mlDeleteNetwork(self._internal)

    def mlSaveNetwork(self, path):
        """

        @param path:
        """
        self._plugin.mlSaveNetwork(self._internal, path)

    def mlLoadNetwork(self, path):
        """

        @param path:
        """
        self._plugin.mlLoadNetwork(self._internal, path)

    def mlPredict(self, num, sig):
        """

        @param num:
        @param sig:
        """
        self._plugin.mlPredict(self._internal, num, sig)

    def mlGetNetworkOutputLength(self):
        """

        @return:
        """
        return self._plugin.mlGetNetworkOutputLength(self._internal)

    def mlGetNetworkPrediction(self):
        """

        @return:
        """
        return self._plugin.mlGetNetworkPrediction(self._internal)
