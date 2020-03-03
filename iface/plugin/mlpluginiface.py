#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod


class MLPluginIFace:
    """
    Define all methods that a plugin should overwrite
    """

    @abstractmethod
    def mlGetTrainer(self, net, data):
        """

        @param net:
        @param data:
        """
        raise NotImplementedError

    @abstractmethod
    def mlDeleteTrainer(self, trainer):
        """

        @param trainer:
        """
        raise NotImplementedError

    @abstractmethod
    def mlConfigureTrainer(self, trainer, path):
        """

        @param trainer:
        @param path:
        """
        raise NotImplementedError

    @abstractmethod
    def mlIsTrainerRunning(self, trainer):
        """

        @param trainer:
        """
        raise NotImplementedError

    @abstractmethod
    def mlGetTrainerProgress(self, trainer):
        """

        @param trainer:
        """
        raise NotImplementedError

    @abstractmethod
    def mlTrainerRun(self, trainer):
        """

        @param trainer:
        """
        raise NotImplementedError

    @abstractmethod
    def mlGetTrainerError(self, trainer):
        """

        @param trainer:
        """
        raise NotImplementedError

    @abstractmethod
    def mlSaveTrainerProgression(self, trainer, path):
        """

        @param trainer:
        @param path:
        """
        raise NotImplementedError

    @abstractmethod
    def mlGetLoadedTrainer(self):
        """

        """
        raise NotImplementedError

    @abstractmethod
    def mlGetNetwork(self, path):
        """

        @param path:
        """
        raise NotImplementedError

    @abstractmethod
    def mlDeleteNetwork(self, net):
        """

        @param net:
        """
        raise NotImplementedError

    @abstractmethod
    def mlSaveNetwork(self, net, path):
        """

        @param net:
        @param path:
        """
        raise NotImplementedError

    @abstractmethod
    def mlLoadNetwork(self, net, path):
        """

        @param net:
        @param path:
        """
        raise NotImplementedError

    @abstractmethod
    def mlPredict(self, net, num, sig):
        """

        @param net:
        @param num:
        @param sig:
        """
        raise NotImplementedError

    @abstractmethod
    def mlGetNetworkOutputLength(self, net):
        """

        @param net:
        """
        raise NotImplementedError

    @abstractmethod
    def mlGetNetworkPrediction(self, net):
        """

        @param net:
        """
        raise NotImplementedError

    @abstractmethod
    def mlGetNetworkNumberOfLayer(self, network):
        """

        @param network:
        """
        raise NotImplementedError

    @abstractmethod
    def mlGetNetworkNumberOfInput(self, network):
        """

        @param network:
        """
        raise NotImplementedError

    @abstractmethod
    def mlGetLayerNumberOfNeuron(self, network, i):
        """

        @param network:
        @param i:
        """
        raise NotImplementedError

    @abstractmethod
    def mlGetNetworkLayerOutputSignal(self, network, i):
        """

        @param network:
        @param i:
        """
        raise NotImplementedError

    @abstractmethod
    def mlGetNetworkInputSignal(self, network):
        """

        @param network:
        """
        raise NotImplementedError

    @abstractmethod
    def mlGetTrainerUI(self):
        """

        """
        raise NotImplementedError
