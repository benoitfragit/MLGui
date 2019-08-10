#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MLNetworkIFace:
    def mlDeleteNetwork(self):
        raise NotImplementedError

    def mlSaveNetwork(self, path):
        raise NotImplementedError

    def mlLoadNetwork(self, path):
        raise NotImplementedError

    def mlPredict(self, num, sig):
        raise NotImplementedError

    def mlGetNetworkOutputLength(self):
        raise NotImplementedError

    def mlGetNetworkPrediction(self):
        raise NotImplementedError
