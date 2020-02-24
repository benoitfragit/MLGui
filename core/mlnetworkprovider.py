#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Array

class MLNetworkProvider:
    def __init__(self, plugin, manager, network, username, managed = False):
        self._arrays    = None #manager.dict()
        self._managed   = managed
        self._plugin    = plugin
        self._username  = username

        numberOfLayers = self._plugin.mlGetNetworkNumberOfLayer(network)
        numberOfInputs = self._plugin.mlGetNetworkNumberOfInput(network)
        
        # pass a signal for the input and all layer
        self._arrays[0] = manager.list([0] * numberOfInputs)
        for i in range(numberOfLayers):
            numberOfNeurons = self._plugin.mlGetLayerNumberOfNeuron(network, i)
            self._arrays[i+1] = manager.list([0] * numberOfNeurons)

    @property
    def arrays(self):
        return self._arrays

    def mlUpdateNetworkProvider(self, network):
        if network is not None:
            for i in self.arrays.keys():
                signal = None
                if i == 0:
                    signal = self._plugin.mlGetNetworkInputSignal(network)
                else:
                    signal = self._plugin.mlGetNetworkLayerOutputSignal(network, i - 1)
                if signal is not None:
                    self._arrays[i] = signal[:]

    @property
    def username(self):
        return self._username

    @property
    def managed(self):
        return self._managed

    def mlGetScene(self):
        return self._plugin.mlGetNetworkDrawerUI()

    def mlDisplayNetworkDrawerUI(self, scene):
        scene.clear()
        scene.mlOnDisplayNetwork(self)

    def mlUpdateNetworkDrawerUI(self, scene):
        scene.mlOnUpdateNetwork(self)
