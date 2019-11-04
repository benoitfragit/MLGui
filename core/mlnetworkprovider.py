#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Array

class MLNetworkProvider:
    def __init__(self, plugin, network, username, managed = False):
        self._arrays    = {}
        self._managed   = managed
        self._plugin    = plugin
        self._username  = username

        numberOfLayers = self._plugin.mlGetNetworkNumberOfLayer(network)
        numberOfInputs = self._plugin.mlGetNetworkNumberOfInput(network)

        # pass a signal for the input and all layer
        self._arrays[0] = Array('d', numberOfInputs)
        for i in range(numberOfLayers):
            numberOfNeurons = self._plugin.mlGetLayerNumberOfNeuron(network, i)
            self._arrays[i+1] = Array('d', numberOfNeurons)

    @property
    def arrays(self):
        return self._arrays

    def mlUpdateNetworkProvider(self, network):
        if network is not None:
            print "ok 1"
            for i in self.arrays.keys():
                signal = None
                if i == 0:
                    signal = self._plugin.mlGetNetworkInputSignal(network)
                else:
                    signal = self._plugin.mlGetNetworkLayerOutputSignal(network, i - 1)
                if signal is not None:
                    self._arrays[i] = signal[:]

    def mlGetUserName(self):
        return self._username

    @property
    def managed(self):
        return self._managed

    def mlGetNetworkDrawerUI(self):
        return self._plugin.mlGetNetworkDrawerUI()

    def mlDisplayNetworkDrawerUI(self):
        scene = self.mlGetNetworkDrawerUI()

        # clear the scene
        scene.clear()

        # draw the scene
        scene.mlOnDisplayNetwork(self)

    def mlUpdateNetworkDrawerUI(self):
        scene = self.mlGetNetworkDrawerUI()
        scene.mlOnUpdateNetwork(self)
