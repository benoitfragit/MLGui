#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MLPluginIFace:
    def mlGetTrainer(self, net, data):
        raise NotImplementedError

    def mlDeleteTrainer(self, trainer):
        raise NotImplementedError

    def mlConfigureTrainer(self, trainer, path):
        raise NotImplementedError

    def mlIsTrainerRunning(self, trainer):
        raise NotImplementedError

    def mlGetTrainerProgress(self, trainer):
        raise NotImplementedError

    def mlTrainerRun(self, trainer):
        raise NotImplementedError

    def mlGetTrainerError(self, trainer):
        raise NotImplementedError

    def mlGetNetwork(self, path):
        raise NotImplementedError

    def mlDeleteNetwork(self, net):
        raise NotImplementedError

    def mlSaveNetwork(self, net, path):
        raise NotImplementedError

    def mlLoadNetwork(self, net, path):
        raise NotImplementedError

    def mlPredict(self, net, num, sig):
        raise NotImplementedError

    def mlGetNetworkOutputLength(self, net):
        raise NotImplementedError

    def mlGetNetworkPrediction(self, net):
        raise NotImplementedError
