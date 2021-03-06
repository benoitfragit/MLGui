#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Array


class MLNetworkProvider:
    """

    """
    def __init__(self, plugin, manager, network, username, managed=False):
        self._arrays = manager.dict()
        self._managed = managed
        self._username = username

        numberOfLayers = plugin.mlGetNetworkNumberOfLayer(network)
        numberOfInputs = plugin.mlGetNetworkNumberOfInput(network)

        # pass a signal for the input and all layer
        self._arrays[0] = manager.list([0] * numberOfInputs)
        numberOfNeurons = 0
        for i in range(numberOfLayers):
            numberOfNeurons = plugin.mlGetLayerNumberOfNeuron(network, i)
            self._arrays[i + 1] = manager.list([0] * numberOfNeurons)
        # pass a signal for the target signal
        self._arrays[numberOfLayers+1] = manager.list([0] * numberOfNeurons)

    @property
    def arrays(self):
        """

        @return:
        """
        return self._arrays

    def mlUpdateNetworkProvider(self, plugin, network):
        """

        @param plugin:
        @param network:
        """
        if network is not None:
            for i in self.arrays.keys():
                signal = None
                if i == 0:
                    signal = plugin.mlGetNetworkInputSignal(network)
                else:
                    signal = plugin.mlGetNetworkLayerOutputSignal(network, i - 1)
                if signal is not None:
                    self._arrays[i] = signal[:]

    @property
    def username(self):
        """

        @return:
        """
        return self._username

    @property
    def managed(self):
        """

        @return:
        """
        return self._managed

    def mlDisplayNetworkDrawerUI(self, scene):
        """

        @param scene:
        """
        scene.clear()
        scene.mlOnDisplayNetwork(self)

    def mlUpdateNetworkDrawerUI(self, scene):
        """

        @param scene:
        """
        scene.mlOnUpdateNetwork(self)
