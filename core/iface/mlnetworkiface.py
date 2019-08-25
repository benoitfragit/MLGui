#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

class MLNetworkIFace:
    @abstractmethod
    def mlDeleteNetwork(self):
        raise NotImplementedError

    @abstractmethod
    def mlSaveNetwork(self, path):
        raise NotImplementedError

    @abstractmethod
    def mlLoadNetwork(self, path):
        raise NotImplementedError

    @abstractmethod
    def mlPredict(self, num, sig):
        raise NotImplementedError

    @abstractmethod
    def mlGetNetworkOutputLength(self):
        raise NotImplementedError

    @abstractmethod
    def mlGetNetworkPrediction(self):
        raise NotImplementedError
