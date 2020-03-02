#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod


class MLPluginIFace:
    """
    Define all methods that a plugin should overwrite
    """

    @abstractmethod
    def mlGetTrainer(self, net, data):
        raise NotImplementedError

    @abstractmethod
    def mlDeleteTrainer(self, trainer):
        raise NotImplementedError

    @abstractmethod
    def mlConfigureTrainer(self, trainer, path):
        raise NotImplementedError

    @abstractmethod
    def mlIsTrainerRunning(self, trainer):
        raise NotImplementedError

    @abstractmethod
    def mlGetTrainerProgress(self, trainer):
        raise NotImplementedError

    @abstractmethod
    def mlTrainerRun(self, trainer):
        raise NotImplementedError

    @abstractmethod
    def mlGetTrainerError(self, trainer):
        raise NotImplementedError

    @abstractmethod
    def mlSaveTrainerProgression(self, trainer, path):
        raise NotImplementedError

    @abstractmethod
    def mlGetLoadedTrainer(self):
        raise NotImplementedError

    @abstractmethod
    def mlGetNetwork(self, path):
        raise NotImplementedError

    @abstractmethod
    def mlDeleteNetwork(self, net):
        raise NotImplementedError

    @abstractmethod
    def mlSaveNetwork(self, net, path):
        raise NotImplementedError

    @abstractmethod
    def mlLoadNetwork(self, net, path):
        raise NotImplementedError

    @abstractmethod
    def mlPredict(self, net, num, sig):
        raise NotImplementedError

    @abstractmethod
    def mlGetNetworkOutputLength(self, net):
        raise NotImplementedError

    @abstractmethod
    def mlGetNetworkPrediction(self, net):
        raise NotImplementedError

    @abstractmethod
    def mlGetNetworkNumberOfLayer(self, network):
        raise NotImplementedError

    @abstractmethod
    def mlGetNetworkNumberOfInput(self, network):
        raise NotImplementedError

    @abstractmethod
    def mlGetLayerNumberOfNeuron(self, network, i):
        raise NotImplementedError

    @abstractmethod
    def mlGetNetworkLayerOutputSignal(self, network, i):
        raise NotImplementedError

    @abstractmethod
    def mlGetNetworkInputSignal(self, network):
        raise NotImplementedError

    @abstractmethod
    def mlGetTrainerUI(self):
        raise NotImplementedError
